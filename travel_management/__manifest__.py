# -*- coding: utf-8 -*-
{
    'name': "Travel Management",
    'version': '16.0.1.0.0',
    'author': "Cybrosys_Technologies",
    'category': 'Sales',
    'summary': 'Travel Management Application',
    'description': """
     Details about travel management and packages details
    """,
    'depends': ['base', 'mail', 'account', 'contacts', 'website'],
    'data': [
        'security/travel_management_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/service_types_demo_data.xml',
        'data/travel_facilities_demo_data.xml',
        'data/schedule_expiry_date.xml',
        'views/travel_booking_view.xml',
        'views/travel_service_view.xml',
        'views/travel_facilities_view.xml',
        'views/travel_vehicle_view.xml',
        'views/vehicle_charges_view.xml',
        'views/tour_package_view.xml',
        'views/website_booking_form_view.xml',
        'wizards/travel_management_report_view.xml',
        'reports/travel_management_template_reports.xml',
        'reports/report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'travel_management/static/src/js/action_manager.js']
    },
    'license': 'AGPL-3',
}
