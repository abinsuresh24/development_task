# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape
from odoo.exceptions import ValidationError


class XLSXReportController(http.Controller):
    """Class defined for connecting frontend and backend"""

    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name):
        """Function creating response and error"""
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = http.serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
        return request.make_response(html_escape(json.dumps(error)))


class TravelBooking(http.Controller):
    """Class declared for creating travel booking from the frontend
    and pass the record to backend"""

    @http.route('/travel_booking_web', type='http', auth='public', website=True)
    def travel_booking_web(self):
        """Function defined for passing records to the front end"""
        customer = request.env['res.partner'].sudo().search([])
        source_country = request.env['res.country'].sudo().search([])
        destination_country = request.env['res.country'].sudo().search([])
        field_service = request.env['travel.service'].sudo().search([])
        values = {

            'customer_id': customer,
            'destination_country_id': destination_country,
            'source_country_id': source_country,
            'field_service_id': field_service,
        }
        return http.request.render("travel_management.travel_booking_website",
                                   values)

    @http.route('/create/travel_booking', type='http', auth='public',
                website=True)
    def create_travel_booking(self, **kw):
        """Function defined for creating records from the front end"""
        field_service = int(kw['field_service_id'])
        booking_details = {
            'customer_id': kw.get('customer_id'),
            'passengers': kw.get('passengers'),
            'source_country_id': kw.get('source_country_id'),
            'destination_country_id': kw.get('destination_country_id'),
            'service': kw.get('service'),
            'field_service_id': field_service,
            'travel_date': kw.get('travel_date')
        }
        if booking_details['customer_id'] == "0":
            raise ValidationError("PLEASE CHOOSE A CUSTOMER")
        if booking_details['source_country_id'] == "0":
            raise ValidationError("PLEASE CHOOSE SOURCE COUNTRY")
        if booking_details['destination_country_id'] == "0":
            raise ValidationError("PLEASE CHOOSE DESTINATION COUNTRY")
        if booking_details['service'] == "0":
            raise ValidationError("PLEASE CHOOSE A SERVICE")
        if booking_details['field_service_id'] == "0":
            raise ValidationError("PLEASE CHOOSE A FIELD SERVICE")
        request.env['travel.booking'].sudo().create(booking_details)
        return request.render("travel_management.booking_success")


class CreateCustomer(http.Controller):
    """Class declared for creating customer from the frontend
        and pass the record to backend"""

    @http.route('/create_customer', type='http', auth='public', website=True)
    def customer_web(self):
        """Function defined for frontend view"""
        return http.request.render("travel_management.create_customer_website")

    @http.route('/create/create_customer', type='http', auth='public',
                website=True)
    def create_customer(self, **kw):
        """Function defined for creating new customers from the frontend"""
        partner = {
            'name': kw.get('customer_id'),
            'street': kw.get('address'),
            'phone': kw.get('phone'),
            'email': kw.get('email')
        }
        request.env['res.partner'].sudo().create(partner)
        return request.render("travel_management.customer_success",
                              {'type': 'ir.actions.client', 'tag': 'reload'})
