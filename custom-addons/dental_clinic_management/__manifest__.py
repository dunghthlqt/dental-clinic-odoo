# -*- coding: utf-8 -*-
{
    'name': 'Clinic Management',
    'version': '1.0',
    'summary': 'Hệ thống quản lý phòng khám nha khoa - Clinic Management System',
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
