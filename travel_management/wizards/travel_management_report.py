from odoo import fields, models


class TravelManagementReport(models.TransientModel):
    _name = 'travel.management.report'
    _description = 'Travel Management Report wizard'

    partner_id = fields.Many2one('res.partner', string="Customer")
    date_from = fields.Date(string="Date from")
    date_to = fields.Date(string="Date to")

    def create_pdf(self):
        query = """select res_partner.name,start_date,end_date,vehicle_type from 
        tour_package INNER JOIN res_partner on  res_partner.id=tour_package.customer_id"""
        self.env.cr.execute(query)
        self.env.cr.fetchall()
        data = {'form_data': self.read()[0]}
        return self.env.ref(
            'travel_management.action_report_travel_management').report_action(
            self, data=data)
