# -*- coding: utf-8 -*-
{
    'name': 'Dental Patient Inquiry Management',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/CRM',
    'summary': 'Simplified CRM for dental clinic - Manage patient inquiries from initial contact to conversion',
    'description': """
Dental Patient Inquiry Management
==================================
This module extends Odoo CRM to manage dental patient inquiries:
- Capture inquiries from phone, Facebook, website
- Schedule consultations
- Track follow-ups
- Convert inquiries to patients
- Integration with dental clinic management module

Key Features:
- Dental-specific inquiry fields
- Consultation scheduling
- Conversion to patient workflow
- Calendar integration for appointments
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'crm',
        'calendar',
        'contacts',
        'mail',
    ],
    'data': [
        # Security must be loaded first
        'security/dental_security.xml',
        'security/ir.model.access.csv',
        'security/dental_record_rules.xml',
        # Data
        'data/crm_team_data.xml',
        'data/crm_stage_data.xml',
        'data/archive_default_stages.xml',
        'data/crm_lead_server_action.xml',
        # Views
        'views/crm_lead_views.xml',
        'views/calendar_event_views.xml',
        'views/res_partner_views.xml',
        # All menus consolidated in one file to ensure correct loading order
        'views/inquiry_menus.xml',
        # Wizard view (action/menu moved to inquiry_menus.xml)
        'wizard/assign_team_wizard_views.xml',
        # Force update views (must be loaded last to override any cached views)
        'data/update_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dental_inquiry/static/src/js/kanban_disable_drag.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
}

