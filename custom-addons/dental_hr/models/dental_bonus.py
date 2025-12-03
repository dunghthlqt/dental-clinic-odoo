# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DentalBonus(models.Model):
    _name = 'dental.bonus'
    _description = 'Dental Bonus'
    _order = 'date desc, id desc'
    
    name = fields.Char('Tên thưởng', required=True)
    
    bonus_type = fields.Selection([
        ('individual', 'Thưởng cá nhân'),
        ('team', 'Thưởng tập thể'),
        ('holiday', 'Thưởng lễ'),
        ('month_13', 'Lương tháng 13'),
        ('other', 'Khác'),
    ], string='Loại thưởng', required=True, default='individual')
    
    amount = fields.Float('Số tiền', required=True)
    
    employee_ids = fields.Many2many(
        'hr.employee',
        'bonus_employee_rel',
        'bonus_id',
        'employee_id',
        string='Nhân viên',
        help='Chọn nhân viên được thưởng (để trống nếu là thưởng tập thể)'
    )
    
    date = fields.Date('Ngày áp dụng', required=True, default=fields.Date.today)
    
    description = fields.Text('Mô tả')
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
    ], string='Trạng thái', default='draft', readonly=True)
    
    # Computed fields
    employee_count = fields.Integer(
        'Số nhân viên',
        compute='_compute_employee_count',
        store=False
    )
    
    @api.depends('employee_ids')
    def _compute_employee_count(self):
        """Tính số nhân viên được thưởng"""
        for bonus in self:
            bonus.employee_count = len(bonus.employee_ids)
    
    def action_confirm(self):
        """Xác nhận thưởng"""
        self.write({'state': 'confirmed'})
    
    def action_draft(self):
        """Quay lại nháp"""
        self.write({'state': 'draft'})

