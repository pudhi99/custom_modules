# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_expiring_lots = fields.Boolean(
        compute='_compute_has_expiring_lots', store=False,
        help='True if any move line has a RED or EXPIRED lot.')

    @api.depends('move_line_ids.lot_id', 'move_line_ids.lot_id.expiry_status')
    def _compute_has_expiring_lots(self):
        for picking in self:
            picking.has_expiring_lots = any(
                ml.lot_id and ml.lot_id.expiry_status in ('red', 'expired')
                for ml in picking.move_line_ids
            )

    def action_sort_fifo(self):
        """Re-sort move lines for each product oldest-expiry-first (FEFO)."""
        self.ensure_one()
        lines_by_product = {}
        for line in self.move_line_ids:
            key = line.product_id.id
            lines_by_product.setdefault(key, []).append(line)

        sequence = 1
        for product_lines in lines_by_product.values():
            product_lines.sort(
                key=lambda l: l.lot_id.expiration_date or fields.Datetime.now()
            )
            for line in product_lines:
                line.sequence = sequence
                sequence += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('FIFO Sort Applied'),
                'message': _('Move lines have been sorted oldest-expiry-first.'),
                'type': 'success',
                'sticky': False,
            },
        }

    def _check_expired_lots(self):
        """Block expired lots on OUTGOING deliveries only.
        Internal transfers (clearance moves) are explicitly allowed."""
        for picking in self:
            if picking.picking_type_code != 'outgoing':
                continue
            expired = [
                ml.lot_id.name
                for ml in picking.move_line_ids
                if ml.lot_id and ml.lot_id.expiry_status == 'expired'
            ]
            if expired:
                raise UserError(
                    _('The following lots are EXPIRED and cannot be shipped:\n%s')
                    % '\n'.join(expired)
                )

    def button_validate(self):
        self._check_expired_lots()
        return super().button_validate()
