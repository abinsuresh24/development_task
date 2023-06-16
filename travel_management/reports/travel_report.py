# -*- coding: utf-8 -*-
from odoo import api, models


class TravelManagementReport(models.AbstractModel):
    """Class defined for travel management report"""
    _name = 'report.travel_management.report_travel_management'
    _description = "report travel details"

    @api.model
    def _get_report_values(self, docids, data=None):
        """Function defined for abstract model"""
        docids = data['form_data']['partner_id']
        travel_data = data['travel_data']
        docs = self.env['tour.package'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'tour.package',
            'data': data,
            'docs': docs,
            'travel_data': travel_data
        }
