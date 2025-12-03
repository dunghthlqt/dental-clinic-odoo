# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dental_supply_count = fields.Integer(
        'Số lượng vật tư nha khoa',
        compute='_compute_dental_supply_count',
        help='Số lượng vật tư nha khoa trong đơn mua này'
    )

    @api.depends('order_line.product_id.is_dental_supply')
    def _compute_dental_supply_count(self):
        """Đếm số lượng vật tư nha khoa trong PO"""
        for order in self:
            order.dental_supply_count = len([
                line for line in order.order_line
                if line.product_id and line.product_id.is_dental_supply
            ])

    def action_view_dental_supplies(self):
        """Mở view hiển thị dental supplies trong PO"""
        self.ensure_one()
        action = {
            'name': 'Vật tư nha khoa',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order.line',
            'view_mode': 'tree,form',
            'domain': [
                ('order_id', '=', self.id),
                ('product_id.is_dental_supply', '=', True)
            ],
            'context': {'create': False},
        }
        return action

