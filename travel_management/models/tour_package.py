# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import MissingError


class TourPackage(models.Model):
    """Class created for adding tour package details"""
    _name = "tour.package"
    _description = "Details about tour packages"
    _rec_name = 'customer_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner', string="Customer",
                                  help="Name of the Customer")
    quotation_date = fields.Date(string="Quotation date", help="Quotation date")
    source_country_id = fields.Many2one('res.country', string="Source location",
                                        help="Starting location"
                                             " of your journey")
    destination_country_id = fields.Many2one('res.country',
                                             string="Destination location",
                                             help="Destination location "
                                                  "of your journey")
    start_date = fields.Date(string="Start date",
                             help="Date which your journey starts")
    end_date = fields.Date(string="End date",
                           help="Date which your journey ends")
    number_of_travellers = fields.Integer(string="Number of travellers",
                                          default=1,
                                          help="Total number of travellers "
                                               "for the travel")
    facilities_id = fields.Many2many('travel.facilities', string="Facilities",
                                     help="Facilities that you can specify")
    vehicle_type = fields.Selection(
        [('bus', 'Bus'), ('traveller', 'Traveller'), ('van', 'Van'),
         ('others', 'Others')], string="Vehicle type",
        help="Choose the vehicle for your travel package")
    vehicle_list_id = fields.Many2one('travel.vehicle', string="Vehicle list",
                                      domain="[('start_date', '=', start_date), "
                                             "('end_date', '=', end_date),"
                                             "('number_of_seats', '=', number_of_travellers),"
                                             "('facilities_ids', '=',facilities_id),"
                                             "('vehicle_type', '=', vehicle_type)]",
                                      help="Available vehicles for the package")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')],
                             string='State', default='draft')
    estimation_km = fields.Float(string="Estimated KM",
                                 help="Estimated kilometer of the package")
    vehicle_charges_ids = fields.One2many('travel.charges',
                                          'service_charges1_id',
                                          string="Service charges")
    package_estimation_amount = fields.Float(string="Estimation amount",
                                             help="Estimated amount of the "
                                                  "travel package")
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string='User',
                              default=lambda self: self.env.user)

    def tour_package_confirm(self):
        """Declaring function for changing the state to confirmed and also
        create a booking automatically while clicking the button CONFIRM"""
        self.state = 'confirmed'
        if self.vehicle_list_id.state == "not_available":
            raise MissingError(
                "There is no vehicle available for this package!")
        self.vehicle_list_id.state = "not_available"
        create_booking = self.env['travel.booking'].create({
            'customer_id': self.customer_id.id,
            'source_country_id': self.source_country_id.id,
            'destination_country_id': self.destination_country_id.id,
            'travel_date': self.start_date,
            'estimation_amount': self.package_estimation_amount})
        return create_booking
