# -*- coding: utf-8 -*-
{
    'name': 'Dental CRM',
    'version': '1.0',
    'summary': 'Quản lý phòng khám nha khoa',
    'author': 'Your Company',
    'category': 'Healthcare',
    'depends': ['base', 'mail'],
    'data': [
        'security/dental_security.xml',
        'security/ir.model.access.csv',
        'views/dental_patient_views.xml',
        'views/dental_treatment_views.xml',
        'views/treatment_session_views.xml',
        'views/dental_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
