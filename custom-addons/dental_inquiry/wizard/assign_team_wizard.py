# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AssignTeamWizard(models.TransientModel):
    _name = 'dental.inquiry.assign.team.wizard'
    _description = 'Assign Dental Inquiry Team to Leads'
    
    def action_assign_team(self):
        """Assign all leads to Dental Inquiry Team"""
        self.ensure_one()
        
        # Find dental inquiry team
        dental_team = self.env['crm.team'].search([
            ('name', '=', 'Đội Inquiry Nha khoa')
        ], limit=1)
        
        if not dental_team:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': 'Không tìm thấy team "Đội Inquiry Nha khoa". Vui lòng update module trước.',
                    'type': 'danger',
                    'sticky': False,
                }
            }
        
        # Find all leads without team or with wrong team
        leads = self.env['crm.lead'].search([
            ('type', '=', 'lead'),
            '|',
            ('team_id', '=', False),
            ('team_id', '!=', dental_team.id)
        ])
        
        if not leads:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'message': 'Tất cả inquiries đã thuộc team đúng.',
                    'type': 'success',
                    'sticky': False,
                }
            }
        
        # Assign team
        leads.write({'team_id': dental_team.id})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã gán {len(leads)} inquiries vào team "Đội Inquiry Nha khoa".',
                'type': 'success',
                'sticky': False,
            }
        }

