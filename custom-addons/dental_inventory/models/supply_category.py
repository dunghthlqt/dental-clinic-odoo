# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DentalSupplyCategory(models.Model):
    _name = 'dental.supply.category'
    _description = 'Phân loại vật tư nha khoa'
    _parent_name = 'parent_id'
    _parent_store = True
    _order = 'parent_path, name'

    name = fields.Char(
        'Tên phân loại',
        required=True,
        translate=True
    )
    code = fields.Char(
        'Mã phân loại',
        help='Mã phân loại vật tư (tùy chọn)'
    )
    parent_id = fields.Many2one(
        'dental.supply.category',
        string='Phân loại cha',
        ondelete='cascade',
        help='Phân loại cha (để tạo cấu trúc phân cấp)'
    )
    child_ids = fields.One2many(
        'dental.supply.category',
        'parent_id',
        string='Phân loại con'
    )
    parent_path = fields.Char(index=True)
    
    product_count = fields.Integer(
        'Số lượng vật tư',
        compute='_compute_product_count',
        help='Số lượng vật tư thuộc phân loại này'
    )

    @api.depends('child_ids', 'product_count')
    def _compute_product_count(self):
        """Tính số lượng vật tư trong category (bao gồm cả category con)"""
        for category in self:
            # Đếm products trực tiếp thuộc category này
            products = self.env['product.product'].search_count([
                ('supply_category_id', '=', category.id),
                ('is_dental_supply', '=', True)
            ])
            
            # Đếm products trong các category con
            child_products = 0
            for child in category.child_ids:
                child_products += child.product_count
            
            category.product_count = products + child_products

    def name_get(self):
        """Hiển thị tên category với parent path"""
        result = []
        for category in self:
            name = category.name
            if category.parent_id:
                name = f"{category.parent_id.name} / {name}"
            result.append((category.id, name))
        return result

