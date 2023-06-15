# -*- coding: utf-8 -*-
from odoo import fields, models


class TravelManagementReport(models.TransientModel):
    """Class defined for creating wizard for report"""
    _name = 'travel.management.report'
    _description = 'Travel Management Report wizard'

    partner_id = fields.Many2one('res.partner', string="Customer",
                        help="Filter the report with the specified customer")
    date_from = fields.Date(string="Date from",
                            help="Filter the report with the specified to date")
    date_to = fields.Date(string="Date to",
                          help="Filter the report with the specified from date")

    def create_pdf(self):
        """Function defined for creating PDF report on the button"""
        query = """select p.name as customer,t.start_date,t.end_date,
                t.vehicle_type,t.state,c.name AS source_country,d.name as
                destination_country from tour_package as t
                INNER JOIN res_partner as p on  p.id=t.customer_id
                join res_country as c on c.id=t.source_country_id
    		    join res_country as d on d.id = t.destination_country_id
    		    where 1=1 """
        if self.partner_id:
            query += """and p.name = '%s'""" % self.partner_id.name
        if self.date_to:
            query += """and t.start_date <= '%s'""" % self.date_to
        if self.date_from:
            query += """and t.end_date >= '%s'""" % self.date_from
        self.env.cr.execute(query)
        travel_data = self.env.cr.dictfetchall()
        data = {'form_data': self.read()[0],
                'travel_data': travel_data}
        return self.env.ref(
            'travel_management.action_report_travels_management').report_action(
            self, data=data)
