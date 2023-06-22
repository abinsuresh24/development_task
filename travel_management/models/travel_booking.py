# -*- coding: utf-8 -*-
import datetime
import dateutil
from odoo import api, fields, models, _


class TravelBooking(models.Model):
    """Class defined for adding Travel booking details"""
    _name = "travel.booking"
    _description = "Booking details"
    _order = "travel_date"
    _rec_name = "booking_ref"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    booking_ref = fields.Char(string="Booking reference",
                              help="Booking reference for each booking",
                              readonly=True,
                              tracking=True, default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string="Customer", help="Name")
    address_id = fields.Char(related='customer_id.contact_address')
    passengers = fields.Integer(string="Passengers", help="No.of passengers",
                                default=1)
    service = fields.Selection([('flight', 'Flight'), ('train', 'Train'),
                                ('bus', 'Bus')], string="Service",
                               help="service method")
    booking_date = fields.Date(string="Booking date",
                               default=fields.Date.today())
    source_country_id = fields.Many2one('res.country', string="Source Location",
                                        help=" Current Country")
    destination_country_id = fields.Many2one('res.country',
                                             string="Destination Country",
                                             help="Destination Location")
    travel_date = fields.Datetime(string="Travel date", help="Travelling date")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('expired', 'Expired')],
                             string='State', readonly=False, copy=False,
                             default='draft')
    expiration_date = fields.Date(string="Expiration date",
                                  help="Expiration of the booking period",
                                  compute="_compute_expiry_date", store=True)
    field_service_id = fields.Many2one('travel.service', string="Field service")
    estimation_amount = fields.Float(string="Estimation amount",
                                     help="Estimated amount for the package")
    fees_and_charges = fields.Float(string="Fees/Charges",
                                    help="Fees and charges of the travel")
    description = fields.Char(compute="_compute_description")
    company_id = fields.Many2one('res.company', string="Company name",
                                 help="Company name",
                                 default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', 'Current User',
                              default=lambda self: self.env.user)

    @api.model
    def create(self, vals_list):
        """Declaring function for creating unique sequence number
        for each booking"""
        if vals_list.get('booking_ref', 'New') == 'New':
            vals_list['booking_ref'] = self.env['ir.sequence'].next_by_code(
                'travel.booking.sequence') or 'New'
        result = super().create(vals_list)
        return result

    def travel_booking_confirm(self):
        """Declaring function for changing the state to confirmed
        while clicking the button CONFIRM"""
        self.write({'state': 'confirmed'})

    @api.depends('field_service_id')
    def _compute_expiry_date(self):
        """Declaring the function for calculating the expiration date"""
        for rec in self:
            exp_period = rec.field_service_id.expiration_period
            print(exp_period, "11111")
            booking_date = datetime.datetime.strptime(str(rec.booking_date),
                                                      "%Y-%m-%d")
            if rec.field_service_id.period_states == 'days':
                expiry_date = booking_date + datetime.timedelta(days=exp_period)
                rec.expiration_date = expiry_date
            elif rec.field_service_id.period_states == 'months':
                expiry_date = booking_date + dateutil.relativedelta.relativedelta(
                    months=exp_period)
                rec.expiration_date = expiry_date
            elif rec.field_service_id.period_states == 'year':
                expiry_date = booking_date + dateutil.relativedelta.relativedelta(
                    years=exp_period)
                rec.expiration_date = expiry_date
        if self.expiration_date and self.expiration_date <= fields.date.today():
            self.write({'state': 'expired'})

    @api.depends('description')
    def _compute_description(self):
        for i in self:
            i.description = i.booking_ref + ' ' + str(i.service)

    def auto_expiration_date(self):
        """Function declared for auto scheduling expiry date"""
        self.env['travel.booking'].search(
            [('expiration_date', '=', fields.date.today()),
             ('state', '=', 'draft')]).write(
            {'state': 'expired'})

    def travel_create_invoice(self):
        """Function defined for creating invoice for booking"""
        if self.service is False:
            invoice = self.env['account.move'].create(
                {'move_type': 'out_invoice',
                 'partner_id': self.customer_id.id,
                 'state': 'draft',
                 'invoice_date': fields.Date.today(),
                 'invoice_line_ids': [
                     fields.Command.create({'name': self.state,
                                            'price_unit': self.estimation_amount})]
                 })
        else:
            invoice = self.env['account.move'].create(
                {'move_type': 'out_invoice',
                 'partner_id': self.customer_id.id,
                 'state': 'draft',
                 'invoice_date': fields.Date.today(),
                 'invoice_line_ids': [
                     fields.Command.create({'name': self.description,
                                            'price_unit': self.fees_and_charges})]
                 })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'move_type': 'out_invoice',
            'res_id': invoice.id,
            'target': 'current'
        }
