# -*- coding: utf-8 -*-
from odoo import models, fields

class SupplyUsage(models.Model):
    _name = 'supply.usage'
    _description = 'Vật tư sử dụng'

    session_id = fields.Many2one('treatment.session', string='Buổi điều trị', required=True, ondelete='cascade')
    supply_code = fields.Char('Mã vật tư')
    name = fields.Char('Tên vật tư', required=True)
    quantity = fields.Integer('Số lượng sử dụng', default=1)
    notes = fields.Char('Ghi chú')
