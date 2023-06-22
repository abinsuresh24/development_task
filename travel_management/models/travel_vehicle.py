# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TravelVehicle(models.Model):
    """Class defined for adding travel vehicle details"""
    _name = "travel.vehicle"
    _description = "Details about vehicles used for travels"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'registration_no'
    _sql_constraints = [('registration_no_unique', 'unique(registration_no)',
                         'Registration number has to be unique!')]

    registration_no = fields.Char(string="Registration number",
                                  help="Registration number of the vehicle")
    vehicle_type = fields.Selection(
        [('bus', 'Bus'), ('traveller', 'Traveller'), ('van', 'Van'),
         ('others', 'Others')], help="Vehicle types")
    vehicle_name = fields.Char(string="Name", compute="compute_vehicle_name",
                               help="Name of the vehicle Registration number + vehicle type")
    number_of_seats = fields.Integer(string="Number of seats", default=1,
                                     help="Number of seats in the selected vehicle")
    facilities_ids = fields.Many2many('travel.facilities', string="Facilities",
                                      help="facilities in the vehicle")
    travel_service_charges_ids = fields.One2many('travel.charges',
                                                 'service_charges_id',
                                                 string="Service charges")
    state = fields.Selection(
        [('available', 'Available'), ('not_available', 'Not available')],
        string="state", compute="compute_state", store=True)
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")

    @api.depends('vehicle_name')
    def compute_vehicle_name(self):
        """function for concatenating Registration number and vehicle type"""
        for rec in self:
            rec.vehicle_name = rec.registration_no + " " + rec.vehicle_type

    @api.depends('end_date')
    def compute_state(self):
        """Function for changing the state on its end date"""
        for rec in self:
            if rec.end_date == fields.date.today():
                rec.state = 'available'
