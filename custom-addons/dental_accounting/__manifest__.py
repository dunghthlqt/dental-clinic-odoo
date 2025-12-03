# -*- coding: utf-8 -*-
{
    'name': 'Dental Accounting',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Accounting',
    'summary': 'Accounting integration for dental clinic',
    'description': """
Dental Accounting Module
========================
This module integrates accounting functionality with dental clinic management:
- Payment Plan for installment treatments (12 months)
- Invoice generation from payments (proof of payment)
- Follow-up for overdue payments (installment treatments only)
- Recurring payments for fixed costs
- Profit calculation and reporting
- Financial reports customized for dental clinic

Key Features:
- Payment policies: Full payment vs Installment
- Payment Plan: 50% upfront, 12 months flexible payment
- Automatic invoice creation from payments
- Follow-up tracking for overdue payments
- Profit calculation: Revenue - Supply Cost - Other Costs
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'account',
        'analytic',
        'dental_clinic_management',
        'mail',
    ],
    'data': [
        # Security must be loaded first (registers models)
        'security/dental_accounting_security.xml',
        # Security CSV (after security XML to ensure models are registered)
        'security/ir.model.access.csv',
        # Wizard views (must be loaded after models are registered)
        'wizard/account_lock_date_views.xml',
        'wizard/payment_wizard_views.xml',
        # Data (must be loaded after models are registered)
        'data/followup_levels.xml',
        'data/payment_plan_data.xml',
        'data/recurring_entry_cron.xml',
        # Views (must be loaded after data to ensure records exist)
        'views/dental_treatment_views.xml',
        'views/payment_plan_views.xml',
        'views/invoice_views.xml',
        'views/followup_views.xml',
        'views/recurring_payments_views.xml',
        'views/profit_report_views.xml',
        # Menu (must be loaded after all views and actions)
        'views/accounting_menu.xml',
        # Reports
        'reports/profit_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dental_accounting/static/src/css/hide_unallocated_credit.css',
            'dental_accounting/static/src/js/hide_unallocated_credit.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

