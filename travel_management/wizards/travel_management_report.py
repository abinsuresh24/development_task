# -*- coding: utf-8 -*-
import io
import json
from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class TravelManagementReport(models.TransientModel):
    """Class defined for creating wizard for report"""
    _name = 'travel.management.report'
    _description = 'Travel Management Report wizard'

    partner_id = fields.Many2one('res.partner', string="Customer",
                                 help="Filter the report with the specified "
                                      "customer")
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string="Date from",
                            help="Filter the report with the specified to date")
    date_to = fields.Date(string="Date to",
                          help="Filter the report with the specified from date")

    def create_pdf(self):
        """Function defined for creating PDF report on the button"""
        if self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')

        query = """select p.name as customer,t.start_date,t.end_date,f.name,
                    t.vehicle_type,t.state,c.name AS source_country,d.name 
                    as destination_country from tour_package as t
                    INNER JOIN res_partner as p on  p.id=t.customer_id
                    join res_country as c on c.id=t.source_country_id
                    join res_country as d on d.id = t.destination_country_id
					join res_company as f on f.id=t.company_id
                    where 1=1"""
        if self.partner_id:
            query += """and p.name = '%s'""" % self.partner_id.name
        if self.date_to:
            query += """and t.start_date <= '%s'""" % self.date_to
        if self.date_from:
            query += """and t.end_date >= '%s'""" % self.date_from
        if self.company_id:
            query +="""and f.name ='%s'"""% self.company_id.name
        self.env.cr.execute(query)
        travel_data = self.env.cr.dictfetchall()
        data = {'form_data': self.read()[0],
                'travel_data': travel_data}
        return self.env.ref(
            'travel_management.action_report_travels_management').report_action(
            self, data=data)

    def print_xlsx(self):
        """Function defined for creating XLSX report on button click"""
        if self.date_from > self.date_to:
            raise ValidationError('Start Date must be less than End Date')
        query = """select p.name as customer,t.start_date,t.end_date,f.name,
                    t.vehicle_type,t.state,c.name AS source_country,d.name 
                    as destination_country from tour_package as t
                    INNER JOIN res_partner as p on  p.id=t.customer_id
                    join res_country as c on c.id=t.source_country_id
                    join res_country as d on d.id = t.destination_country_id
					join res_company as f on f.id=t.company_id
                    where 1=1"""
        if self.partner_id:
            query += """and p.name = '%s'""" % self.partner_id.name
        if self.date_to:
            query += """and t.start_date <= '%s'""" % self.date_to
        if self.date_from:
            query += """and t.end_date >= '%s'""" % self.date_from
        if self.company_id:
            query +="""and f.name ='%s'"""% self.company_id.name
        self.env.cr.execute(query)
        travel_data = self.env.cr.dictfetchall()
        data = {'form_data': self.read()[0],
                'travel_data': travel_data}
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'travel.management.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """Function defined for XLSX report view"""
        partner = data['form_data']['partner_id']
        from_date = data['form_data']['date_from']
        to_date = data['form_data']['date_to']
        travel_data = data['travel_data']
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format(
            {'font_size': '12px', 'bold': True, 'align': 'center'})
        sheet.merge_range('I2:P3', "Travels Management Report", head)
        sheet.merge_range('A6:B6', 'Customer:', txt)
        if self.partner_id:
            sheet.merge_range('C6:D6', partner[1], cell_format)
        sheet.merge_range('A7:B7', 'From Date:', txt)
        if self.date_from:
            sheet.merge_range('C7:D7', from_date, cell_format)
        sheet.merge_range('A8:B8', 'To Date:', txt)
        if self.date_to:
            sheet.merge_range('C8:D8', to_date, cell_format)
        sheet.write('B12', 'Sl. No', txt)
        sheet.merge_range('C12:E12', 'Source Location', txt)
        sheet.merge_range('F12:H12', ' Destination Location', txt)
        sheet.merge_range('I12:J12', 'Vehicle Name', txt)
        sheet.merge_range('K12:L12', 'State', txt)
        sl_no = 0
        row = 12
        for rec in travel_data:
            sl_no += 1
            sheet.write(row, 1, sl_no, cell_format)
            sheet.merge_range(row, 2, row, 4, rec['source_country']['en_US'],
                              cell_format)
            sheet.merge_range(row, 5, row, 7,
                              rec['destination_country']['en_US'], cell_format)
            sheet.merge_range(row, 8, row, 9, rec['vehicle_type'], cell_format)
            sheet.merge_range(row, 10, row, 11, rec['state'], cell_format)
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
