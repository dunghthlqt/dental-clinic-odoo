#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để fix external IDs trong views đã lưu trong database
Chạy script này trong Odoo shell để cập nhật các view có external ID không đầy đủ

Usage:
    odoo shell -d your_database_name < scripts/fix_view_groups.py
"""

import re

# Tìm tất cả các view có external ID không đầy đủ
views = env['ir.ui.view'].search([
    '|', '|',
    ('arch_db', 'ilike', '%groups="group_dental_inquiry_receptionist%'),
    ('arch_db', 'ilike', '%groups="group_dental_inquiry_dentist%'),
    ('arch_db', 'ilike', '%groups="group_dental_inquiry_manager%'),
])

print(f"Tìm thấy {len(views)} views cần cập nhật")

for view in views:
    arch_db = view.arch_db
    if not arch_db:
        continue
    
    arch_str = arch_db
    original_arch = arch_str
    
    # Replace external IDs
    arch_str = re.sub(
        r'groups="group_dental_inquiry_receptionist([,"])',
        r'groups="dental_inquiry.group_dental_inquiry_receptionist\1',
        arch_str
    )
    arch_str = re.sub(
        r'groups="group_dental_inquiry_dentist([,"])',
        r'groups="dental_inquiry.group_dental_inquiry_dentist\1',
        arch_str
    )
    arch_str = re.sub(
        r'groups="group_dental_inquiry_manager([,"])',
        r'groups="dental_inquiry.group_dental_inquiry_manager\1',
        arch_str
    )
    
    # Replace trong comma-separated lists
    arch_str = re.sub(
        r',group_dental_inquiry_receptionist([,"])',
        r',dental_inquiry.group_dental_inquiry_receptionist\1',
        arch_str
    )
    arch_str = re.sub(
        r',group_dental_inquiry_dentist([,"])',
        r',dental_inquiry.group_dental_inquiry_dentist\1',
        arch_str
    )
    arch_str = re.sub(
        r',group_dental_inquiry_manager([,"])',
        r',dental_inquiry.group_dental_inquiry_manager\1',
        arch_str
    )
    
    if arch_str != original_arch:
        view.arch_db = arch_str
        print(f"Đã cập nhật view: {view.name} (ID: {view.id})")
    else:
        print(f"View {view.name} (ID: {view.id}) không cần cập nhật")

env.cr.commit()
print("Hoàn thành! Đã cập nhật tất cả views.")

