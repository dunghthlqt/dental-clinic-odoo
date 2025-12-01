# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'
    
    appointment_type = fields.Selection([
        ('consultation', 'Tư vấn (Bán hàng)'),
        ('treatment', 'Buổi điều trị'),
        ('followup', 'Tái khám'),
        ('emergency', 'Cấp cứu'),
        ('other', 'Khác')
    ], string='Loại lịch hẹn', default='other', help='Loại lịch hẹn')
    
    lead_id = fields.Many2one('crm.lead', string='Inquiry liên quan', help='Inquiry liên quan đến appointment này')
    treatment_session_id = fields.Many2one('treatment.session', string='Buổi điều trị', help='Buổi điều trị liên quan (nếu có)')
    
    patient_id = fields.Many2one('res.partner', string='Bệnh nhân', compute='_compute_patient', store=True, help='Bệnh nhân (từ partner)')
    
    @api.depends('lead_id', 'treatment_session_id', 'partner_ids')
    def _compute_patient(self):
        """Compute patient from lead, treatment session, or partner_ids"""
        for event in self:
            if event.treatment_session_id:
                # Get partner from dental.patient
                dental_patient = event.treatment_session_id.patient_id
                # Try to get partner from dental patient (if integration exists)
                if hasattr(dental_patient, 'partner_id') and dental_patient.partner_id:
                    event.patient_id = dental_patient.partner_id
                else:
                    event.patient_id = False
            elif event.lead_id:
                event.patient_id = event.lead_id.partner_id
            elif event.partner_ids:
                event.patient_id = event.partner_ids[0]
            else:
                event.patient_id = False

