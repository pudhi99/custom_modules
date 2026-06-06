# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockExpirySendAlert(models.TransientModel):
    _name = 'stock.expiry.send.alert'
    _description = 'Send Expiry Alert Now Wizard'

    lot_ids = fields.Many2many(
        'stock.lot', string='Lots',
        default=lambda self: self._default_lot_ids())
    alert_type = fields.Selection([
        ('email', 'Email'),
        ('inbox', 'Odoo Inbox'),
        ('both', 'Email + Inbox'),
    ], string='Alert Channel', default='email', required=True)
    recipient_ids = fields.Many2many(
        'res.users', string='Recipients',
        default=lambda self: self._default_recipients())
    custom_message = fields.Text(string='Custom Message (optional)')

    def _default_lot_ids(self):
        lot_ids = self.env.context.get('default_lot_ids', [])
        return self.env['stock.lot'].browse(lot_ids)

    def _default_recipients(self):
        config = self.env['stock.expiry.config'].get_config()
        return config.alert_recipient_ids

    def action_send(self):
        self.ensure_one()
        if not self.lot_ids:
            raise UserError(_('Please select at least one lot.'))
        if not self.recipient_ids:
            raise UserError(_('Please select at least one recipient.'))

        now = fields.Datetime.now()
        try:
            template = self.env.ref('stock_expiry_alert_manager.mail_template_expiry_manual')
        except Exception:
            template = None

        for lot in self.lot_ids:
            if self.alert_type in ('email', 'both') and template:
                for user in self.recipient_ids:
                    template.with_context(
                        recipient_user=user,
                        lot=lot,
                        custom_message=self.custom_message,
                    ).send_mail(lot.id, force_send=True, email_values={
                        'email_to': user.email,
                    })

            if self.alert_type in ('inbox', 'both'):
                body = _('⚠️ Expiry Alert: Lot <b>%s</b> expires on %s (%d days remaining).') % (
                    lot.name,
                    lot.expiration_date.strftime('%Y-%m-%d') if lot.expiration_date else '?',
                    lot.days_to_expiry,
                )
                if self.custom_message:
                    body += '<br/>' + self.custom_message
                lot.message_post(
                    body=body,
                    partner_ids=self.recipient_ids.mapped('partner_id').ids,
                    subtype_xmlid='mail.mt_comment',
                )

            lot.write({
                'alert_count': lot.alert_count + 1,
                'last_alert_date': now,
            })
            self.env['stock.expiry.history'].create({
                'lot_id': lot.id,
                'expiration_date': lot.expiration_date,
                'days_to_expiry': lot.days_to_expiry,
                'expiry_status': lot.expiry_status,
                'alert_type': self.alert_type,
                'alert_level': 'manual',
                'recipient_ids': [(6, 0, self.recipient_ids.ids)],
                'notes': self.custom_message or '',
                'company_id': lot.company_id.id,
            })

        return {'type': 'ir.actions.act_window_close'}
