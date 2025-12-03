# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_dental_supply = fields.Boolean(
        'Là vật tư nha khoa',
        default=False,
        help='Đánh dấu sản phẩm này là vật tư tiêu hao dùng trong điều trị'
    )

    supply_category_id = fields.Many2one(
        'dental.supply.category',
        string='Phân loại vật tư',
        help='Phân loại vật tư nha khoa'
    )

    min_stock_level = fields.Float(
        'Mức tồn kho tối thiểu',
        default=0.0,
        help='Cảnh báo khi tồn kho dưới mức này'
    )

    is_low_stock = fields.Boolean(
        'Tồn kho thấp',
        compute='_compute_is_low_stock',
        store=False,  # Cannot store because qty_available is also computed
        help='True nếu tồn kho < min_stock_level. Chỉ hiển thị trong form view, không thể search.'
    )

    @api.depends('qty_available', 'min_stock_level', 'is_dental_supply')
    def _compute_is_low_stock(self):
        """Tính toán xem tồn kho có thấp không"""
        for product in self:
            if product.is_dental_supply and product.min_stock_level > 0:
                product.is_low_stock = product.qty_available < product.min_stock_level
            else:
                product.is_low_stock = False

    @api.model
    def default_get(self, fields_list):
        """Set default values khi tạo product mới"""
        res = super().default_get(fields_list)
        
        # Nếu đang tạo từ dental supply context
        if self.env.context.get('default_is_dental_supply'):
            res['type'] = 'product'  # Storable - để có thể track tồn kho
            res['tracking'] = 'none'  # Không tracking lot, chỉ quản lý số lượng
            res['is_dental_supply'] = True
            # Vật tư nha khoa không bán ra, chỉ mua vào
            res['sale_ok'] = False
            res['purchase_ok'] = True  # Vẫn cần mua vào
        
        return res

    @api.onchange('is_dental_supply')
    def _onchange_is_dental_supply(self):
        """Tự động set type khi đánh dấu là dental supply"""
        if self.is_dental_supply:
            self.type = 'product'  # Storable - để có thể track tồn kho
            self.tracking = 'none'  # Không tracking lot, chỉ quản lý số lượng
            # Vật tư nha khoa không bán ra, chỉ mua vào
            self.sale_ok = False
            self.purchase_ok = True  # Vẫn cần mua vào
        else:
            # Nếu bỏ check is_dental_supply, có thể giữ tracking như cũ
            pass

    def write(self, vals):
        """Override để đảm bảo type = 'product' và tracking = 'none' khi is_dental_supply = True"""
        # Nếu đang set is_dental_supply = True, đảm bảo type = 'product' và tracking = 'none'
        if vals.get('is_dental_supply'):
            vals['type'] = 'product'  # Storable - để có thể track tồn kho
            vals['tracking'] = 'none'
        
        result = super().write(vals)
        
        # Sau khi write, nếu is_dental_supply = True, đảm bảo type = 'product' và tracking = 'none'
        for product in self:
            if product.is_dental_supply:
                updates = {}
                if product.type != 'product':
                    updates['type'] = 'product'  # Storable - để có thể track tồn kho
                if product.tracking != 'none':
                    updates['tracking'] = 'none'
                if updates:
                    product.write(updates)
        
        return result

