# -*- coding: utf-8 -*-
{
    'name': 'Dental HR Management',
    'version': '17.0.1.0.0',
    'category': 'Human Resources/Dental',
    'summary': 'Quản lý nhân viên nha khoa, tính lương và thưởng',
    'description': """
Dental HR Management
====================

Module quản lý nhân viên nha khoa, tích hợp với module HR gốc của Odoo:
* Quản lý thông tin nhân viên nha khoa (bác sĩ, kỹ thuật viên, lễ tân, kế toán, quản lý kho)
* Quản lý nghỉ phép (tích hợp hr_holidays)
* Tính lương và thưởng linh hoạt
* Tích hợp với dental_accounting để tạo bút toán kế toán
* Hiển thị chi phí lương trong báo cáo lợi nhuận
    """,
    'author': 'Dental Clinic',
    'website': '',
    'depends': [
        'base',
        'hr',
        'hr_contract',
        'hr_holidays',
        'account',
    ],
    'data': [
        # Security groups (must be loaded first)
        'security/dental_hr_security.xml',
        # Views (load before CSV to ensure models are registered - views trigger model loading)
        'views/dental_role_views.xml',
        'views/dental_bonus_views.xml',
        'views/dental_salary_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_employee_leaves_button.xml',  # Load after hr_employee_views.xml to ensure models are loaded
        # Security CSV (load after views to ensure models are registered)
        'security/ir.model.access.csv',
        # Data (load after security to ensure access rights are set)
        'data/dental_role_data.xml',
        'data/salary_journal_data.xml',
        # Menu (must be loaded after all views and actions)
        'views/hr_menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

