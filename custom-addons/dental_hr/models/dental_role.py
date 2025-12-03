# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DentalRole(models.Model):
    _name = 'dental.role'
    _description = 'Vai trò nhân viên nha khoa'
    _order = 'name'

    name = fields.Char(
        'Tên vai trò',
        required=True,
        translate=True
    )
    
    code = fields.Char(
        'Mã vai trò',
        required=True,
        copy=False,
        help='Mã định danh vai trò (ví dụ: doctor, technician)'
    )
    
    description = fields.Text(
        'Mô tả',
        translate=True
    )
    
    employee_ids = fields.Many2many(
        'hr.employee',
        'employee_role_rel',
        'role_id',
        'employee_id',
        string='Nhân viên',
        help='Danh sách nhân viên có vai trò này'
    )
    
    employee_count = fields.Integer(
        'Số nhân viên',
        compute='_compute_employee_count',
        store=False
    )
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Mã vai trò phải là duy nhất!')
    ]
    
    @api.depends('employee_ids')
    def _compute_employee_count(self):
        """Tính số lượng nhân viên có vai trò này"""
        for role in self:
            role.employee_count = len(role.employee_ids)
    
    def action_view_employees(self):
        """Mở danh sách nhân viên có vai trò này"""
        self.ensure_one()
        action = {
            'name': 'Nhân viên - %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'view_mode': 'tree,form',
            'domain': [('dental_roles', 'in', [self.id])],
            'context': {'default_dental_roles': [(4, self.id)]},
        }
        return action

