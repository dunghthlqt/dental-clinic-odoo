# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DentalTreatment(models.Model):
    _name = 'dental.treatment'
    _description = 'Hồ sơ điều trị nha khoa'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên hồ sơ', required=True, tracking=True)
    active = fields.Boolean('Active', default=True)
    medical_record_code = fields.Char('Mã hồ sơ', readonly=True, copy=False)
    patient_id = fields.Many2one('dental.patient', string='Bệnh nhân', required=True, tracking=True)
    doctor_id = fields.Many2one('res.users', string='Bác sĩ phụ trách', tracking=True, domain=lambda self: [('groups_id', 'in', [self.env.ref('dental_crm.group_dental_doctor').id])])
    is_doctor = fields.Boolean('Is Doctor', compute='_compute_is_doctor')
    is_technician_or_doctor = fields.Boolean('Is Technician or Doctor', compute='_compute_is_technician_or_doctor')
    treatment_type = fields.Selection([
        ('orthodontics', 'Niềng răng'),
        ('filling', 'Trám răng'),
        ('extraction', 'Nhổ răng'),
        ('whitening', 'Tẩy trắng'),
        ('implant', 'Cấy ghép'),
        ('other', 'Khác'),
    ], string='Loại điều trị', tracking=True)
    status = fields.Selection([
        ('information', 'Lấy thông tin'),
        ('examination', 'Khám lâm sàng'),
        ('consultation', 'Tư vấn'),
        ('planning', 'Lên kế hoạch'),
        ('in_progress', 'Đang điều trị'),
        ('follow_up', 'Tái khám'),
        ('completed', 'Hoàn thành'),
    ], string='Trạng thái', default='information', tracking=True)
    payment_status = fields.Selection([
        ('unpaid', 'Chưa thanh toán'),
        ('partial', 'Thanh toán một phần'),
        ('paid', 'Đã thanh toán'),
    ], string='Trạng thái thanh toán', default='unpaid', tracking=True, readonly=True)
    start_date = fields.Date('Ngày bắt đầu', tracking=True)
    end_date = fields.Date('Ngày kết thúc dự kiến', tracking=True)
    session_ids = fields.One2many('treatment.session', 'treatment_id', string='Buổi điều trị')
    session_count = fields.Integer('Số buổi', compute='_compute_session_count')
    total_cost = fields.Float('Tổng chi phí', tracking=True, default=0.0)
    paid_amount = fields.Float('Đã thanh toán', tracking=True, default=0.0, readonly=True)
    notes = fields.Text('Ghi chú')

    @api.model
    def create(self, vals):
        if not vals.get('medical_record_code'):
            vals['medical_record_code'] = self.env['ir.sequence'].next_by_code('dental.treatment') or 'DT000'
        return super(DentalTreatment, self).create(vals)

    def _compute_session_count(self):
        for record in self:
            record.session_count = len(record.session_ids)

    @api.depends_context('uid')
    def _compute_is_doctor(self):
        doctor_group = self.env.ref('dental_crm.group_dental_doctor')
        for record in self:
            record.is_doctor = doctor_group in self.env.user.groups_id

    @api.depends_context('uid')
    def _compute_is_technician_or_doctor(self):
        technician_group = self.env.ref('dental_crm.group_dental_technician')
        doctor_group = self.env.ref('dental_crm.group_dental_doctor')
        for record in self:
            record.is_technician_or_doctor = (technician_group in self.env.user.groups_id) or (doctor_group in self.env.user.groups_id)
