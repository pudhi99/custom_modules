# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockExpiryCostReport(models.Model):
    """Aggregated cost-at-risk snapshot per expiry tier.
    Refreshed by the compute cron; read-only for users."""
    _name = 'stock.expiry.cost.report'
    _description = 'Expiry Cost-at-Risk Report'
    _order = 'report_date desc, expiry_status'
    _rec_name = 'report_date'

    report_date = fields.Date(string='Report Date', required=True, default=fields.Date.today)
    expiry_status = fields.Selection([
        ('green', 'Green (Safe)'),
        ('yellow', 'Yellow (Warning)'),
        ('red', 'Red (Critical)'),
        ('expired', 'Expired'),
    ], string='Expiry Tier', required=True)
    lot_count = fields.Integer(string='Lots / Serials')
    product_count = fields.Integer(string='Distinct Products')
    total_qty = fields.Float(string='Total Quantity')
    total_cost = fields.Float(string='Total Cost at Risk', digits=(16, 2))
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company)

    @api.model
    def refresh_report(self, company_id=None):
        """Re-compute today's cost-at-risk snapshot. Called by cron."""
        if not company_id:
            company_id = self.env.company.id
        today = fields.Date.today()
        # Remove today's existing records for this company
        self.search([
            ('company_id', '=', company_id),
            ('report_date', '=', today),
        ]).unlink()

        lots = self.env['stock.lot'].search([
            ('company_id', '=', company_id),
            ('expiry_status', '!=', False),
        ])

        tier_data = {}
        for lot in lots:
            status = lot.expiry_status or 'green'
            if status not in tier_data:
                tier_data[status] = {
                    'lot_ids': set(),
                    'product_ids': set(),
                    'total_qty': 0.0,
                    'total_cost': 0.0,
                }
            tier_data[status]['lot_ids'].add(lot.id)
            tier_data[status]['product_ids'].add(lot.product_id.id)
            qty = lot.product_qty
            cost = qty * (lot.product_id.standard_price or 0.0)
            tier_data[status]['total_qty'] += qty
            tier_data[status]['total_cost'] += cost

        for status, data in tier_data.items():
            self.create({
                'report_date': today,
                'expiry_status': status,
                'lot_count': len(data['lot_ids']),
                'product_count': len(data['product_ids']),
                'total_qty': data['total_qty'],
                'total_cost': data['total_cost'],
                'company_id': company_id,
            })
