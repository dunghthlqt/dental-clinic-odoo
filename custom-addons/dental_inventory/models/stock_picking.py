# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    supplier_id = fields.Many2one(
        'res.partner',
        string='Nhà cung cấp',
        domain=[('is_company', '=', True), ('supplier_rank', '>', 0)],
        help='Nhà cung cấp vật tư (cho Incoming picking)'
    )

    is_dental_supply_receipt = fields.Boolean(
        'Là nhập kho vật tư nha khoa',
        compute='_compute_is_dental_supply_receipt',
        help='True nếu tất cả products trong picking là dental supplies'
    )

    dental_supply_count = fields.Integer(
        'Số lượng vật tư nha khoa',
        compute='_compute_dental_supply_count',
        help='Số lượng vật tư nha khoa trong picking này'
    )

    @api.depends('move_ids_without_package.product_id.is_dental_supply')
    def _compute_is_dental_supply_receipt(self):
        """Tính toán xem picking có phải là nhập kho vật tư nha khoa không"""
        for picking in self:
            if not picking.move_ids_without_package:
                picking.is_dental_supply_receipt = False
                continue

            all_dental_supplies = all(
                move.product_id.is_dental_supply 
                for move in picking.move_ids_without_package 
                if move.product_id
            )
            picking.is_dental_supply_receipt = all_dental_supplies

    @api.depends('move_ids_without_package.product_id.is_dental_supply')
    def _compute_dental_supply_count(self):
        """Đếm số lượng vật tư nha khoa trong picking"""
        for picking in self:
            picking.dental_supply_count = len([
                move for move in picking.move_ids_without_package
                if move.product_id and move.product_id.is_dental_supply
            ])

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        """Tự động fill supplier_id từ purchase order"""
        if self.purchase_id and self.purchase_id.partner_id:
            self.supplier_id = self.purchase_id.partner_id.id

