# -*- coding: utf-8 -*-
from odoo import models, fields

class TreatmentSession(models.Model):
    _name = 'treatment.session'
    _description = 'Buổi điều trị'
    _order = 'session_date desc'

    active = fields.Boolean('Active', default=True)
    treatment_id = fields.Many2one('dental.treatment', string='Hồ sơ điều trị', required=True, ondelete='cascade')
    patient_id = fields.Many2one('dental.patient', related='treatment_id.patient_id', string='Bệnh nhân', store=True)
    session_date = fields.Date('Ngày thực hiện', required=True)
    doctor_ids = fields.Many2many('res.users', string='Bác sĩ/Nhân viên')
    notes = fields.Text('Ghi chú điều trị')
    notes_en = fields.Text('Ghi chú (EN)')
    status = fields.Selection([
        ('scheduled', 'Đã lên lịch'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ], string='Trạng thái', default='scheduled')
    supply_ids = fields.One2many('supply.usage', 'session_id', string='Vật tư sử dụng')
    next_appointment = fields.Char('Lịch hẹn tiếp theo')
    next_appointment_date = fields.Date('Ngày hẹn tiếp theo')

    def write(self, vals):
        result = super(TreatmentSession, self).write(vals)
        # Tự động tạo buổi điều trị mới khi hoàn thành và có lịch hẹn
        for record in self:
            if record.status == 'completed' and record.next_appointment_date:
                # Kiểm tra xem đã có buổi điều trị với ngày này chưa
                existing = self.search([
                    ('treatment_id', '=', record.treatment_id.id),
                    ('session_date', '=', record.next_appointment_date),
                    ('id', '!=', record.id)
                ])
                if not existing:
                    self.create({
                        'treatment_id': record.treatment_id.id,
                        'session_date': record.next_appointment_date,
                        'status': 'scheduled',
                        'notes': 'Tự động tạo từ lịch hẹn trước',
                    })
        return result
