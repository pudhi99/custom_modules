# -*- coding: utf-8 -*-
import logging
from datetime import timedelta

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class StockLot(models.Model):
    _inherit = 'stock.lot'

    # --- Our 8 new fields ---
    expiry_status = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('expired', 'Expired'),
    ], string='Expiry Status', compute='_compute_expiry_status', store=True,
        help='Traffic-light status based on days remaining until expiration_date.')
    days_to_expiry = fields.Integer(
        string='Days to Expiry', compute='_compute_expiry_status', store=True)
    estimated_cost = fields.Float(
        string='Estimated Cost', compute='_compute_estimated_cost', store=True, digits=(16, 2),
        help='On-hand quantity × product standard price.')
    auto_transfer_created = fields.Boolean(
        string='Auto Transfer Created', default=False, copy=False,
        help='Prevents duplicate clearance transfers for this lot.')
    skip_alert_until = fields.Datetime(
        string='Snooze Alerts Until', copy=False,
        help='Suppress alerts until this datetime (snooze).')
    alert_count = fields.Integer(
        string='Alerts Sent', default=0, copy=False,
        help='Total number of alerts sent for this lot.')
    last_alert_date = fields.Datetime(
        string='Last Alert Date', copy=False)
    alert_level_sent = fields.Selection([
        ('level_1', 'Level 1 (30d)'),
        ('level_2', 'Level 2 (15d)'),
        ('level_3', 'Level 3 (7d)'),
        ('level_4', 'Level 4 (3d)'),
        ('level_5', 'Level 5 (1d)'),
    ], string='Highest Alert Level Sent', copy=False)

    # Convenience: alert history
    expiry_history_ids = fields.One2many(
        'stock.expiry.history', 'lot_id', string='Alert History')
    expiry_history_count = fields.Integer(
        compute='_compute_expiry_history_count', string='Alert Count')

    @api.depends('expiry_history_ids')
    def _compute_expiry_history_count(self):
        for lot in self:
            lot.expiry_history_count = len(lot.expiry_history_ids)

    @api.depends('expiration_date')
    def _compute_expiry_status(self):
        now = fields.Datetime.now()
        config = self.env['stock.expiry.config'].get_config()
        green_days = config.threshold_green
        yellow_days = config.threshold_yellow
        red_days = config.threshold_red

        for lot in self:
            if not lot.expiration_date:
                lot.days_to_expiry = 0
                lot.expiry_status = False
                continue
            delta = lot.expiration_date - now
            days = delta.days
            lot.days_to_expiry = days
            if days < 0:
                lot.expiry_status = 'expired'
            elif days < red_days:
                lot.expiry_status = 'red'
            elif days < yellow_days:
                lot.expiry_status = 'yellow'
            else:
                lot.expiry_status = 'green'

    @api.depends('product_qty', 'product_id.standard_price')
    def _compute_estimated_cost(self):
        for lot in self:
            lot.estimated_cost = lot.product_qty * (lot.product_id.standard_price or 0.0)

    # -------------------------------------------------------------------------
    # CRON 1: compute expiry status + auto-create clearance transfers
    # -------------------------------------------------------------------------
    @api.model
    def _cron_compute_expiry_status(self):
        """Recompute expiry_status on all lots and auto-create clearance transfers.
        Iterates over every company config so multi-company setups work correctly."""
        all_configs = self.env['stock.expiry.config'].sudo().search([])

        for config in all_configs:
            company = config.company_id
            lots = self.sudo().with_company(company).search([
                ('expiration_date', '!=', False),
                ('company_id', '=', company.id),
            ])
            if not lots:
                continue

            lots._compute_expiry_status()
            lots._compute_estimated_cost()

            if config.auto_transfer_enabled and config.clearance_location_id:
                red_lots = lots.filtered(
                    lambda l: l.expiry_status == 'red' and not l.auto_transfer_created)
                for lot in red_lots:
                    self.sudo().with_company(company)._create_clearance_transfer(lot, config)

        # Refresh cost-at-risk report for all companies
        self.env['stock.expiry.cost.report'].sudo().refresh_report()

    def _create_clearance_transfer(self, lot, config):
        """Create a draft internal transfer to clearance location for this lot."""
        quants = self.env['stock.quant'].sudo().search([
            ('lot_id', '=', lot.id),
            ('quantity', '>', 0),
            ('location_id.usage', '=', 'internal'),
            ('location_id', '!=', config.clearance_location_id.id),
        ])
        if not quants:
            _logger.warning('Expiry alert: no quants found for lot %s', lot.name)
            return

        # Get internal picking type via warehouse (handles inactive types too)
        warehouse = self.env['stock.warehouse'].sudo().search([
            ('company_id', '=', lot.company_id.id),
        ], limit=1)
        picking_type = warehouse.int_type_id if warehouse else False
        if not picking_type:
            _logger.warning('Expiry alert: no internal picking type for company %s', lot.company_id.name)
            return

        total_qty = sum(quants.mapped('quantity'))

        picking = self.env['stock.picking'].sudo().create({
            'picking_type_id': picking_type.id,
            'location_id': quants[0].location_id.id,
            'location_dest_id': config.clearance_location_id.id,
            'origin': _('Expiry Alert — %s') % lot.name,
            'company_id': lot.company_id.id,
            'move_ids': [(0, 0, {
                'product_id': lot.product_id.id,
                'product_uom': lot.product_uom_id.id,
                'product_uom_qty': total_qty,
                'location_id': quants[0].location_id.id,
                'location_dest_id': config.clearance_location_id.id,
            })],
        })

        picking.action_confirm()

        # Force the specific expiring lot onto the move lines (not Odoo's FIFO pick)
        move = picking.move_ids[0]
        move.move_line_ids.unlink()
        for quant in quants:
            self.env['stock.move.line'].sudo().create({
                'move_id': move.id,
                'picking_id': picking.id,
                'product_id': lot.product_id.id,
                'product_uom_id': lot.product_uom_id.id,
                'lot_id': lot.id,
                'quantity': quant.quantity,
                'location_id': quant.location_id.id,
                'location_dest_id': config.clearance_location_id.id,
                'company_id': lot.company_id.id,
            })

        lot.auto_transfer_created = True

        self.env['stock.expiry.history'].create({
            'lot_id': lot.id,
            'expiration_date': lot.expiration_date,
            'days_to_expiry': lot.days_to_expiry,
            'expiry_status': lot.expiry_status,
            'alert_type': 'auto_transfer',
            'transfer_id': picking.id,
            'company_id': lot.company_id.id,
        })
        _logger.info('Expiry alert: created clearance transfer %s for lot %s', picking.name, lot.name)

    # -------------------------------------------------------------------------
    # CRON 2: send daily tiered email alerts
    # -------------------------------------------------------------------------
    @api.model
    def _cron_send_daily_alerts(self):
        """Send tiered email alerts for all companies with configured recipients."""
        now = fields.Datetime.now()
        all_configs = self.env['stock.expiry.config'].sudo().search([])

        for config in all_configs:
            recipients = config.alert_recipient_ids
            if not recipients:
                continue

            company = config.company_id
            alert_levels = [
                ('level_5', config.alert_days_5, 'stock_expiry_alert_manager.mail_template_expiry_level_5'),
                ('level_4', config.alert_days_4, 'stock_expiry_alert_manager.mail_template_expiry_level_4'),
                ('level_3', config.alert_days_3, 'stock_expiry_alert_manager.mail_template_expiry_level_3'),
                ('level_2', config.alert_days_2, 'stock_expiry_alert_manager.mail_template_expiry_level_2'),
                ('level_1', config.alert_days_1, 'stock_expiry_alert_manager.mail_template_expiry_level_1'),
            ]

            for level_key, days, template_ref in alert_levels:
                window_start = now + timedelta(days=days - 1)
                window_end = now + timedelta(days=days + 1)
                lots = self.sudo().with_company(company).search([
                    ('expiration_date', '>=', window_start),
                    ('expiration_date', '<=', window_end),
                    ('expiration_date', '!=', False),
                    ('company_id', '=', company.id),
                ])
                lots = lots.filtered(
                    lambda l: (not l.skip_alert_until or l.skip_alert_until < now)
                    and l.alert_level_sent != level_key
                )
                if not lots:
                    continue

                try:
                    template = self.env.ref(template_ref)
                except Exception:
                    _logger.warning('Expiry alert template %s not found', template_ref)
                    continue

                for lot in lots:
                    for user in recipients:
                        template.sudo().with_context(
                            recipient_user=user,
                            lot=lot,
                        ).send_mail(lot.id, force_send=False, email_values={
                            'email_to': user.email,
                            'email_from': company.email or 'noreply@example.com',
                        })

                    lot.sudo().write({
                        'alert_count': lot.alert_count + 1,
                        'last_alert_date': now,
                        'alert_level_sent': level_key,
                    })
                    self.env['stock.expiry.history'].sudo().create({
                        'lot_id': lot.id,
                        'expiration_date': lot.expiration_date,
                        'days_to_expiry': lot.days_to_expiry,
                        'expiry_status': lot.expiry_status,
                        'alert_type': 'email',
                        'alert_level': level_key,
                        'recipient_ids': [(6, 0, recipients.ids)],
                        'company_id': lot.company_id.id,
                    })
                    _logger.info('Expiry alert %s sent for lot %s (%s)', level_key, lot.name, company.name)

    # -------------------------------------------------------------------------
    # CRON 3: weekly digest (Monday 08:00)
    # -------------------------------------------------------------------------
    @api.model
    def _cron_send_weekly_digest(self):
        """Send weekly digest for all companies with configured recipients."""
        all_configs = self.env['stock.expiry.config'].sudo().search([])

        for config in all_configs:
            recipients = config.digest_recipient_ids or config.alert_recipient_ids
            if not recipients:
                continue

            company = config.company_id
            lots_by_status = {}
            for status in ['expired', 'red', 'yellow', 'green']:
                lots_by_status[status] = self.sudo().with_company(company).search([
                    ('expiry_status', '=', status),
                    ('company_id', '=', company.id),
                ])

            try:
                template = self.env.ref('stock_expiry_alert_manager.mail_template_weekly_digest')
            except Exception:
                _logger.warning('Weekly digest template not found')
                continue

            for user in recipients:
                template.sudo().with_context(
                    recipient_user=user,
                    lots_by_status=lots_by_status,
                ).send_mail(company.id, force_send=False, email_values={
                    'email_to': user.email,
                    'email_from': company.email or 'noreply@example.com',
                })

            self.env['stock.expiry.history'].sudo().create({
                'alert_type': 'digest',
                'alert_level': 'digest',
                'recipient_ids': [(6, 0, recipients.ids)],
                'notes': _('Weekly digest sent to %d recipients') % len(recipients),
                'company_id': company.id,
            })

    def action_send_alert_now(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Send Alert Now'),
            'res_model': 'stock.expiry.send.alert',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lot_ids': self.ids},
        }

    def action_view_alert_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Alert History'),
            'res_model': 'stock.expiry.history',
            'view_mode': 'list,form',
            'domain': [('lot_id', 'in', self.ids)],
        }
