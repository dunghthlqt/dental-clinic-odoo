# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # This field will be used by integration module to link with dental.patient
    # For now, we just add the field structure
    is_dental_patient = fields.Boolean(string='Là bệnh nhân nha khoa', default=False, help='Đánh dấu đây là bệnh nhân nha khoa')
    inquiry_ids = fields.One2many('crm.lead', 'partner_id', string='Các inquiry', help='Các inquiry liên quan đến partner này')

