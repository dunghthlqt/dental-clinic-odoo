# -*- coding: utf-8 -*-
{
    'name': 'Dental Inventory',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Inventory',
    'summary': 'Inventory management for dental clinic supplies',
    'description': """
Dental Inventory Management
============================
Module quản lý vật tư tiêu hao cho phòng khám nha khoa:
- Quản lý danh mục vật tư (Dental Supplies)
- Phân loại vật tư (Supply Categories)
- Tích hợp với Stock và Purchase
- Tự động tính chi phí vật tư từ đơn mua
- Tự động trừ tồn kho khi sử dụng trong điều trị
- Tích hợp với Accounting để tính supply_cost
    """,
    'author': 'Your Company',
    'depends': [
        'base',
        'stock',
        'purchase',
        'dental_clinic_management',
    ],
    'data': [
        'security/dental_inventory_security.xml',
        'security/ir.model.access.csv',
        'data/supply_categories.xml',
        'data/low_stock_alert_cron.xml',
        'views/supply_category_views.xml',
        'views/dental_supply_views.xml',
        'views/supply_usage_views.xml',
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml',
        'views/low_stock_alert_views.xml',
        'views/supply_usage_report_views.xml',
        'views/inventory_menu.xml',
        'reports/supply_usage_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'auto_install': False,
}

