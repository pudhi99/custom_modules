# -*- coding: utf-8 -*-

from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'

    color_scheme = fields.Selection([
        ('system', 'System'),
        ('light', 'Light'),
        ('dark', 'Dark'),
    ], string='Color Scheme', default='system')

    dark_mode_theme = fields.Selection([
        ('dark_default', 'Default Dark'),
        ('dark_midnight', 'Midnight Blue'),
        ('dark_emerald', 'Emerald Forest'),
        ('dark_crimson', 'Royal Red'),
        ('dark_oceanic', 'Oceanic Blue'),
    ], string='Dark Mode Theme', default='dark_default')

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ['color_scheme', 'dark_mode_theme']

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ['color_scheme', 'dark_mode_theme']
