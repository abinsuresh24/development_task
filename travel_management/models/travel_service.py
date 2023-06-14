# -*- coding: utf-8 -*-
from odoo import fields, models


class TravelService(models.Model):
    """Class defined for adding service types"""
    _name = "travel.service"
    _description = "Service period"
    _rec_name = "service_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    service_name = fields.Char(string="Service", required=True, help="Service")
    expiration_period = fields.Integer(string="Expiration period",
                                       help="Expiration of the service")
    period_states = fields.Selection(
        [('days', 'Days'), ('months', 'Months'), ('year', 'Year')],
        string="Period type")
