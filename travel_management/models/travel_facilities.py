# -*- coding: utf-8 -*-
from odoo import fields, models


class TravelFacilities(models.Model):
    """Class created for adding details of travel facilities"""
    _name = "travel.facilities"
    _description = "Details about facilities provided by company"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'facilities'

    facilities = fields.Char(string="Facilities",
                             help="Facilities provided by the travel management")
