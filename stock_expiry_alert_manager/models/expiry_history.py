# -*- coding: utf-8 -*-
from odoo import fields, models


class StockExpiryHistory(models.Model):
    _name = 'stock.expiry.history'
    _description = 'Expiry Alert History'
    _order = 'alert_date desc, id desc'
    _rec_name = 'lot_id'

    lot_id = fields.Many2one('stock.lot', string='Lot/Serial', ondelete='set null', index=True)
    product_id = fields.Many2one('product.product', string='Product', related='lot_id.product_id', store=True)
    expiration_date = fields.Datetime(string='Expiry Date')
    days_to_expiry = fields.Integer(string='Days to Expiry')
    expiry_status = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('expired', 'Expired'),
    ], string='Status at Alert Time')
    alert_type = fields.Selection([
        ('email', 'Email'),
        ('inbox', 'Odoo Inbox'),
        ('both', 'Email + Inbox'),
        ('auto_transfer', 'Auto Transfer Created'),
        ('digest', 'Weekly Digest'),
    ], string='Alert Type', required=True)
    alert_level = fields.Selection([
        ('level_1', 'Level 1 (30d)'),
        ('level_2', 'Level 2 (15d)'),
        ('level_3', 'Level 3 (7d)'),
        ('level_4', 'Level 4 (3d)'),
        ('level_5', 'Level 5 (1d)'),
        ('manual', 'Manual'),
        ('digest', 'Digest'),
    ], string='Alert Level')
    alert_date = fields.Datetime(string='Alert Sent At', default=fields.Datetime.now)
    recipient_ids = fields.Many2many(
        'res.users', 'expiry_history_user_rel', 'history_id', 'user_id',
        string='Recipients')
    transfer_id = fields.Many2one('stock.picking', string='Auto Transfer', ondelete='set null')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company)
