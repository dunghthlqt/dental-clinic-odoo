# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DentalPatient(models.Model):
    _name = 'dental.patient'
    _description = 'Bệnh nhân nha khoa'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Họ và tên', required=True, tracking=True)
    active = fields.Boolean('Active', default=True)
    customer_code = fields.Char('Mã bệnh nhân', readonly=True, copy=False)
    birth_date = fields.Date('Ngày sinh', tracking=True)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ], string='Giới tính', tracking=True)
    phone = fields.Char('Số điện thoại', tracking=True)
    email = fields.Char('Email', tracking=True)
    address = fields.Text('Địa chỉ', tracking=True)
    dental_condition = fields.Text('Tình trạng răng miệng')
    medical_notes = fields.Text('Ghi chú y tế')
    treatment_ids = fields.One2many('dental.treatment', 'patient_id', string='Hồ sơ điều trị')
    treatment_count = fields.Integer('Số lần điều trị', compute='_compute_treatment_count')

    @api.model
    def create(self, vals):
        if not vals.get('customer_code'):
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('dental.patient') or 'BN000'
        return super(DentalPatient, self).create(vals)

    def _compute_treatment_count(self):
        for record in self:
            record.treatment_count = len(record.treatment_ids)
