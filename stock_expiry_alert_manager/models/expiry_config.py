# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockExpiryConfig(models.Model):
    _name = 'stock.expiry.config'
    _description = 'Expiry Alert Configuration'
    _rec_name = 'company_id'

    company_id = fields.Many2one(
        'res.company', string='Company', required=True)

    # Threshold days (configurable)
    threshold_green = fields.Integer(
        string='Green Threshold (days)', default=30,
        help='Lots expiring in more than this many days are GREEN (safe).')
    threshold_yellow = fields.Integer(
        string='Yellow Threshold (days)', default=15,
        help='Lots expiring between yellow and green thresholds are YELLOW (warning).')
    threshold_red = fields.Integer(
        string='Red Threshold (days)', default=7,
        help='Lots expiring in fewer than this many days are RED (critical).')

    # Alert levels - days before expiry to send email
    alert_days_1 = fields.Integer(string='Alert 1 - Days Before Expiry', default=30)
    alert_days_2 = fields.Integer(string='Alert 2 - Days Before Expiry', default=15)
    alert_days_3 = fields.Integer(string='Alert 3 - Days Before Expiry', default=7)
    alert_days_4 = fields.Integer(string='Alert 4 - Days Before Expiry', default=3)
    alert_days_5 = fields.Integer(string='Alert 5 - Days Before Expiry', default=1)

    # Auto-transfer
    auto_transfer_enabled = fields.Boolean(
        string='Auto-create Clearance Transfer', default=True,
        help='When a lot reaches RED status, automatically create a draft internal transfer to the clearance location.')
    clearance_location_id = fields.Many2one(
        'stock.location', string='Clearance Location',
        domain="[('usage', '=', 'internal'), ('company_id', '=', company_id)]",
        help='Destination location for auto-generated clearance transfers.')

    # Recipients
    alert_recipient_ids = fields.Many2many(
        'res.users', 'expiry_config_user_rel', 'config_id', 'user_id',
        string='Alert Recipients',
        help='Users who receive daily expiry alert emails.')
    digest_recipient_ids = fields.Many2many(
        'res.users', 'expiry_config_digest_user_rel', 'config_id', 'user_id',
        string='Weekly Digest Recipients',
        help='Users who receive the Monday weekly digest.')

    # Product category filter
    monitor_category_ids = fields.Many2many(
        'product.category', 'expiry_config_category_rel', 'config_id', 'category_id',
        string='Monitor Categories',
        help='Leave empty to monitor ALL product categories.')

    # Location filter
    monitor_location_ids = fields.Many2many(
        'stock.location', 'expiry_config_location_rel', 'config_id', 'location_id',
        string='Monitor Locations',
        domain="[('usage', '=', 'internal'), ('company_id', '=', company_id)]",
        help='Leave empty to monitor ALL internal locations.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' not in vals:
                vals['company_id'] = self.env.company.id
        return super().create(vals_list)

    @api.model
    def get_config(self, company_id=None):
        if not company_id:
            company_id = self.env.company.id
        config = self.search([('company_id', '=', company_id)], limit=1)
        if not config:
            config = self.create({'company_id': company_id})
        return config

    @api.model
    def action_open_expiry_config(self):
        """Open/create the expiry config for current company."""
        config = self.get_config()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expiry Alert Settings',
            'res_model': 'stock.expiry.config',
            'res_id': config.id,
            'view_mode': 'form',
            'target': 'current',
        }
