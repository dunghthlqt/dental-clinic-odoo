# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    # Quản lý nhiều roles
    dental_roles = fields.Many2many(
        'dental.role',
        'employee_role_rel',
        'employee_id',
        'role_id',
        string='Vai trò',
        help='Nhân viên có thể có nhiều vai trò (ví dụ: Kế toán kiêm Quản lý kho)'
    )
    
    # Thông tin chuyên môn (cho bác sĩ)
    dental_specialty = fields.Selection([
        ('orthodontics', 'Niềng răng'),
        ('implant', 'Cấy ghép'),
        ('whitening', 'Tẩy trắng'),
        ('filling', 'Trám răng'),
        ('extraction', 'Nhổ răng'),
        ('general', 'Tổng quát'),
        ('other', 'Khác'),
    ], string='Chuyên khoa', help='Chuyên khoa của bác sĩ')
    
    years_of_experience = fields.Integer(
        'Số năm kinh nghiệm',
        help='Số năm kinh nghiệm trong ngành nha khoa'
    )
    
    certifications = fields.Text(
        'Bằng cấp/Chứng chỉ',
        help='Bằng cấp và chứng chỉ của nhân viên'
    )
    
    # Computed fields
    salary_count = fields.Integer(
        'Số lần tính lương',
        compute='_compute_salary_count',
        store=False,
        help='Số lần đã tính lương cho nhân viên này'
    )
    
    leave_count = fields.Integer(
        'Số đơn nghỉ phép',
        compute='_compute_leave_count',
        store=False,
        help='Số đơn nghỉ phép của nhân viên này'
    )
    
    def _compute_salary_count(self):
        """Tính số lần đã tính lương cho nhân viên"""
        for employee in self:
            if employee.id:
                employee.salary_count = self.env['dental.salary'].search_count([
                    ('employee_id', '=', employee.id)
                ])
            else:
                employee.salary_count = 0
    
    def _compute_leave_count(self):
        """Tính số đơn nghỉ phép của nhân viên"""
        for employee in self:
            if employee.id:
                # Check if hr.leave model exists (from hr_holidays)
                if 'hr.leave' in self.env:
                    employee.leave_count = self.env['hr.leave'].search_count([
                        ('employee_id', '=', employee.id)
                    ])
                else:
                    employee.leave_count = 0
            else:
                employee.leave_count = 0
    
    def action_view_salaries(self):
        """Mở danh sách lương của nhân viên"""
        self.ensure_one()
        action = {
            'name': 'Lương của %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'dental.salary',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }
        return action
    
    def action_view_leaves(self):
        """Mở danh sách nghỉ phép của nhân viên"""
        self.ensure_one()
        # Check if hr.leave model exists (from hr_holidays)
        if 'hr.leave' not in self.env:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'message': 'Module nghỉ phép chưa được cài đặt.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        action = {
            'name': 'Nghỉ phép của %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }
        return action

