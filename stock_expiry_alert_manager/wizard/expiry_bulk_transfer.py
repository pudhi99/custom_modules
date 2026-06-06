# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockExpiryBulkTransfer(models.TransientModel):
    _name = 'stock.expiry.bulk.transfer'
    _description = 'Bulk Clearance Transfer Wizard'

    status_filter = fields.Selection([
        ('red', 'RED — Critical (< threshold)'),
        ('red_expired', 'RED + EXPIRED'),
        ('yellow', 'YELLOW — Warning'),
        ('all', 'ALL non-green'),
    ], string='Move Lots With Status', default='red', required=True)

    clearance_location_id = fields.Many2one(
        'stock.location', string='Clearance Location', required=True,
        domain="[('usage', '=', 'internal')]")

    lot_ids = fields.Many2many(
        'stock.lot', string='Lots to Move',
        compute='_compute_lot_ids', store=False)

    lot_count = fields.Integer(compute='_compute_lot_ids')
    total_cost = fields.Float(compute='_compute_lot_ids', string='Total Cost at Risk', digits=(16, 2))

    @api.depends('status_filter')
    def _compute_lot_ids(self):
        for wiz in self:
            if wiz.status_filter == 'red':
                statuses = ['red']
            elif wiz.status_filter == 'red_expired':
                statuses = ['red', 'expired']
            elif wiz.status_filter == 'yellow':
                statuses = ['yellow']
            else:
                statuses = ['yellow', 'red', 'expired']

            lots = self.env['stock.lot'].search([
                ('expiry_status', 'in', statuses),
                ('expiration_date', '!=', False),
            ])
            wiz.lot_ids = lots
            wiz.lot_count = len(lots)
            wiz.total_cost = sum(lots.mapped('estimated_cost'))

    def action_create_transfers(self):
        self.ensure_one()
        if not self.lot_ids:
            raise UserError(_('No lots found matching the selected filter.'))

        config = self.env['stock.expiry.config'].get_config()
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('warehouse_id.company_id', '=', self.env.company.id),
        ], limit=1)
        if not picking_type:
            raise UserError(_('No internal transfer type found for this company.'))

        created_pickings = self.env['stock.picking']
        for lot in self.lot_ids:
            quants = self.env['stock.quant'].search([
                ('lot_id', '=', lot.id),
                ('quantity', '>', 0),
                ('location_id.usage', '=', 'internal'),
                ('location_id', '!=', self.clearance_location_id.id),
            ])
            if not quants:
                continue

            move_lines = [(0, 0, {
                'name': lot.product_id.name,
                'product_id': lot.product_id.id,
                'product_uom': lot.product_uom_id.id,
                'product_uom_qty': quant.quantity,
                'location_id': quant.location_id.id,
                'location_dest_id': self.clearance_location_id.id,
                'lot_id': lot.id,
            }) for quant in quants]

            picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'location_id': quants[0].location_id.id,
                'location_dest_id': self.clearance_location_id.id,
                'origin': _('Bulk Expiry Clearance'),
                'move_ids': move_lines,
            })
            created_pickings |= picking
            lot.auto_transfer_created = True

        if not created_pickings:
            raise UserError(_('No transfers could be created (no on-hand stock found).'))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Clearance Transfers'),
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_pickings.ids)],
        }
