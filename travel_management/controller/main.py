# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


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
    @http.route('/travel_booking_web', type='http', auth='public', website=True)
    def travel_booking_web(self):
        customer = request.env['res.partner'].sudo().search([])
        source_country = request.env['res.country'].sudo().search([])
        destination_country = request.env['res.country'].sudo().search([])
        field_service = request.env['travel.service'].sudo().search([])
        # values = {
        #
        #     'customer_id': customer,
        #     'destination_country_id': destination_country,
        #     'source_country_id': source_country,
        #     'field_service_id': field_service,
        # }
        # print(values,'1111111')
        return http.request.render("travel_management.travel_booking_website",
                                   {'customer_id': customer,
                                    'destination_country_id': destination_country,
                                    'source_country_id': source_country,
                                    'field_service_id': field_service})

    @http.route('/create/travel_booking', type='http', auth='public',
                website=True)
    def create_travel_booking(self, **kw):
        request.env['travel.booking'].sudo().create(kw)
        return request.render("travel_management.booking_success", {})
