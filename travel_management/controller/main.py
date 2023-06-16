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
    @http.route('/travel_booking_web', type='http', auth='public', methods=['POST'],
                website=True)
    def travel_booking_web(self, **kw):
        return http.request.render("travel_management.travel_booking", {})
    # @http.route('/create/travel_booking', type='http', auth='public', methods=['POST'],
    #             website=True)
    # def travel_booking(self, **kw):
    #     request.env['travel.booking'].sudo().create(kw)
