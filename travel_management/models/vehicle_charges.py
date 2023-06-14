# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TravelCharges(models.Model):
    """Class for adding vehicle service charges details"""
    _name = "travel.charges"
    _description = "Details about vehicle service details"
    _rec_name = 'vehicle_service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_service = fields.Char(string="Service", help="Service")
    vehicle_quantity = fields.Integer(string="Quantity", default=1,
                                      readonly=True, help="Vehicle quantity")
    vehicle_units = fields.Integer(string="Units", help="Vehicle units")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency',
                                          string="company currency",
                                          related="company_id.currency_id",
                                          readonly=True)
    service_amount = fields.Monetary(string="Amount",
                                     currency_field="company_currency_id")
    service_charges_id = fields.Many2one('travel.vehicle',
                                         string="Service charges")
    service_charges1_id = fields.Many2one('tour.package',
                                          string='service charges1')
    service_subtotal = fields.Float(string="Subtotal",
                                    help="Calculated as Quantity * Amount")

    @api.onchange('service_amount')
    def _onchange_service_subtotal(self):
        """Function defined for computing the subtotal"""
        self.service_subtotal = self.vehicle_quantity * self.service_amount
