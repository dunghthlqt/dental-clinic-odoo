# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.model
    def default_get(self, fields_list):
        """Set default team for dental inquiries"""
        res = super().default_get(fields_list)
        if self._context.get('default_type') == 'lead' or not res.get('type') or res.get('type') == 'lead':
            # Try to get dental inquiry team
            dental_team = self.env['crm.team'].search([
                ('name', '=', 'Đội Inquiry Nha khoa')
            ], limit=1)
            if dental_team and 'team_id' in fields_list:
                res['team_id'] = dental_team.id
            # Set default stage to first stage of dental team
            if dental_team and 'stage_id' in fields_list:
                first_stage = self.env['crm.stage'].search([
                    ('team_id', '=', dental_team.id)
                ], order='sequence', limit=1)
                if first_stage:
                    res['stage_id'] = first_stage.id
        return res
    
    @api.model_create_multi
    def create(self, vals_list):
        """Ensure all leads are assigned to dental inquiry team"""
        # Get dental team
        dental_team = self.env['crm.team'].search([
            ('name', '=', 'Đội Inquiry Nha khoa')
        ], limit=1)
        
        # Assign team to all leads if not set
        for vals in vals_list:
            if vals.get('type') == 'lead' and not vals.get('team_id') and dental_team:
                vals['team_id'] = dental_team.id
                # Also set stage if not set
                if not vals.get('stage_id'):
                    first_stage = self.env['crm.stage'].search([
                        ('team_id', '=', dental_team.id)
                    ], order='sequence', limit=1)
                    if first_stage:
                        vals['stage_id'] = first_stage.id
        
        return super().create(vals_list)
    
    def write(self, vals):
        """Override to detect stage change and auto-create patient when moving to 'Đã tư vấn - Chờ quyết định'
        Also prevent moving to previous stages (only allow forward progression)
        """
        # Prevent moving to previous stages (only allow forward progression)
        if 'stage_id' in vals:
            for record in self:
                # Only process leads (not opportunities)
                if record.type != 'lead':
                    continue
                
                # Get current and new stage
                current_stage = record.stage_id
                new_stage = self.env['crm.stage'].browse(vals['stage_id'])
                
                # Check if trying to move backward (only for leads)
                if current_stage and new_stage:
                    # Get dental inquiry team stages
                    dental_team = self.env['crm.team'].search([
                        ('name', '=', 'Đội Inquiry Nha khoa')
                    ], limit=1)
                    
                    if dental_team:
                        # Check if both stages belong to dental team
                        if (current_stage.team_id == dental_team and 
                            new_stage.team_id == dental_team and 
                            current_stage.sequence > new_stage.sequence):
                            # Prevent backward movement
                            raise UserError(
                                'Không thể chuyển inquiry về stage trước đó. Chỉ cho phép chuyển tiến lên.'
                            )
                
                # Check if moving to "Đã tư vấn - Chờ quyết định"
                if new_stage.name == 'Đã tư vấn - Chờ quyết định' and not self.env.context.get('skip_auto_create_patient'):
                    # Auto-create patient if not already created
                    patient_created = record._auto_create_patient()
                    # Store flag to show notification after write completes
                    if patient_created and record.converted_dental_patient_id:
                        # Store in context for notification (will be processed after write)
                        if not hasattr(self.env, '_dental_patient_created'):
                            self.env._dental_patient_created = []
                        self.env._dental_patient_created.append({
                            'inquiry_id': record.id,
                            'patient_name': record.converted_dental_patient_id.name,
                        })
        
        result = super().write(vals)
        
        # Show notification after successful write
        # Note: This will show in the chatter/message area
        # For popup notification, we need to use JavaScript client action
        if hasattr(self.env, '_dental_patient_created') and self.env._dental_patient_created:
            notifications_to_show = self.env._dental_patient_created.copy()
            # Clear immediately to avoid duplicate
            self.env._dental_patient_created = []
            
            for notification in notifications_to_show:
                inquiry = self.browse(notification['inquiry_id'])
                if inquiry.exists():
                    # Post message to show notification
                    inquiry.message_post(
                        body=f'✅ <strong>Đã tạo hồ sơ bệnh nhân thành công:</strong> {notification["patient_name"]}',
                        message_type='notification',
                    )
        
        return result
    
    def _auto_create_patient(self):
        """Auto-create dental patient when inquiry moves to 'Đã tư vấn - Chờ quyết định'
        
        This method:
        1. Checks if patient already exists (via converted_dental_patient_id)
        2. Searches for existing patient by phone/email
        3. Creates dental.patient if not exists
        4. Links inquiry with patient
        5. Returns True if patient was created, False otherwise
        """
        self.ensure_one()
        
        # Skip if clinic module not installed
        if 'dental.patient' not in self.env:
            return False
        
        # Skip if patient already created for this inquiry
        if self.converted_dental_patient_id:
            return False
        
        # Skip if no contact name (required field)
        if not self.contact_name:
            return False
        
        try:
            # 1. Check if patient already exists (by phone or email)
            domain = []
            if self.phone:
                domain.append(('phone', '=', self.phone))
            elif self.email_from:
                domain.append(('email', '=', self.email_from))
            
            dental_patient = False
            patient_created = False
            if domain:
                dental_patient = self.env['dental.patient'].search(domain, limit=1)
            
            # 2. Create dental.patient if not exists
            if not dental_patient:
                dental_patient_vals = {
                    'name': self.contact_name,
                    'phone': self.phone or '',
                    'email': self.email_from or '',
                    'address': self.street or '',  # Map street from inquiry to address
                }
                
                # Add gender if available
                if self.gender:
                    if hasattr(self.env['dental.patient'], 'gender'):
                        dental_patient_vals['gender'] = self.gender
                
                # Add date of birth if available
                if self.date_of_birth:
                    if hasattr(self.env['dental.patient'], 'birth_date'):
                        dental_patient_vals['birth_date'] = self.date_of_birth
                
                dental_patient = self.env['dental.patient'].create(dental_patient_vals)
                patient_created = True
            
            # 3. Link inquiry with patient
            self.converted_dental_patient_id = dental_patient.id
            
            # 4. Create/update partner if needed
            if not self.partner_id:
                partner_vals = {
                    'name': self.contact_name,
                    'phone': self.phone,
                    'email': self.email_from,
                    'is_company': False,
                }
                # Add street address if available
                if self.street:
                    partner_vals['street'] = self.street
                # Add gender and date of birth if available
                if self.gender and hasattr(self.env['res.partner'], 'gender'):
                    gender_map = {
                        'male': 'male',
                        'female': 'female',
                        'other': 'other'
                    }
                    partner_vals['gender'] = gender_map.get(self.gender, False)
                if self.date_of_birth:
                    if hasattr(self.env['res.partner'], 'date_of_birth'):
                        partner_vals['date_of_birth'] = self.date_of_birth
                    elif hasattr(self.env['res.partner'], 'birthdate'):
                        partner_vals['birthdate'] = self.date_of_birth
                
                partner = self.env['res.partner'].create(partner_vals)
                self.partner_id = partner
                
                # Mark partner as dental patient if field exists
                if hasattr(partner, 'is_dental_patient'):
                    partner.write({'is_dental_patient': True})
            
            return patient_created
            
        except Exception as e:
            # Log error but don't block stage change
            _logger.warning(f"Failed to auto-create patient for inquiry {self.id}: {str(e)}")
            return False
    
    # Override stage_id to only show dental inquiry stages
    stage_id = fields.Many2one(
        'crm.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
        ondelete='restrict',
    )
    
    # Source tracking
    facebook_url = fields.Char(string='Facebook', help='Link Facebook của khách hàng hoặc tin nhắn từ Facebook')
    
    # Personal information
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính', help='Giới tính của khách hàng')
    
    date_of_birth = fields.Date(string='Ngày sinh', help='Ngày sinh của khách hàng')
    
    # Dental-specific inquiry info
    dental_issue = fields.Text(string='Mô tả vấn đề răng miệng', help='Mô tả vấn đề răng miệng của khách hàng')
    treatment_interest = fields.Selection([
        ('orthodontics', 'Niềng răng'),
        ('implant', 'Cấy ghép Implant'),
        ('root_canal', 'Điều trị tủy'),
        ('extraction', 'Nhổ răng'),
        ('restoration', 'Hàn trám'),
        ('cleaning', 'Vệ sinh răng'),
        ('whitening', 'Tẩy trắng'),
        ('other', 'Khác')
    ], string='Loại điều trị quan tâm', help='Loại điều trị khách hàng quan tâm')
    
    urgency_level = fields.Selection([
        ('low', 'Không gấp'),
        ('medium', 'Bình thường'),
        ('high', 'Gấp'),
        ('emergency', 'Cấp cứu')
    ], string='Mức độ khẩn cấp', default='medium', help='Mức độ khẩn cấp')
    
    # Consultation tracking
    consultation_date = fields.Datetime(string='Ngày giờ hẹn tư vấn', help='Ngày giờ hẹn tư vấn')
    consultation_event_id = fields.Many2one('calendar.event', string='Lịch hẹn tư vấn', readonly=True, help='Lịch hẹn tư vấn trong calendar')
    consultation_notes = fields.Text(string='Ghi chú tư vấn', help='Ghi chú sau khi tư vấn')
    estimated_treatment_value = fields.Float(string='Chi phí điều trị ước tính', help='Chi phí điều trị ước tính (VND)')
    
    # Conversion tracking
    converted_patient_id = fields.Many2one('res.partner', string='Đã chuyển đổi thành bệnh nhân', readonly=True, help='Partner record sau khi convert')
    converted_dental_patient_id = fields.Many2one('dental.patient', string='Bệnh nhân đã chuyển đổi', readonly=True, help='Bệnh nhân trong hệ thống clinic')
    treatment_case_id = fields.Many2one('dental.treatment', string='Hồ sơ điều trị', readonly=True, help='Hồ sơ điều trị được tạo từ inquiry này')
    
    # Computed
    is_high_value = fields.Boolean(compute='_compute_is_high_value', store=True, string='Inquiry giá trị cao', help='Inquiry có giá trị cao (>= 20 triệu)')
    
    @api.depends('estimated_treatment_value')
    def _compute_is_high_value(self):
        """Compute if inquiry is high value (>= 20 million VND)"""
        for lead in self:
            lead.is_high_value = lead.estimated_treatment_value >= 20000000
    
    @api.onchange('estimated_treatment_value')
    def _onchange_estimated_treatment_value(self):
        """Auto-update expected_revenue when estimated_treatment_value changes"""
        if self.estimated_treatment_value:
            self.expected_revenue = self.estimated_treatment_value
    
    def action_schedule_consultation(self):
        """Create consultation appointment in calendar"""
        self.ensure_one()
        
        if not self.consultation_date:
            # Default to tomorrow at 9 AM if not set
            tomorrow = fields.Datetime.now() + timedelta(days=1)
            self.consultation_date = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        
        event = self.env['calendar.event'].create({
            'name': f'Tư vấn: {self.contact_name or self.name}',
            'start': self.consultation_date,
            'stop': self.consultation_date + timedelta(hours=1),
            'partner_ids': [(4, self.partner_id.id)] if self.partner_id else [],
            'lead_id': self.id,
            'appointment_type': 'consultation',
            'description': f'Tư vấn cho inquiry: {self.name}\nVấn đề răng miệng: {self.dental_issue or "N/A"}',
        })
        
        self.consultation_event_id = event.id
        
        # Update stage if consultation is scheduled
        # Find stage by name and team (if team exists)
        domain = [('name', '=', 'Đã đặt lịch tư vấn')]
        if self.team_id:
            domain.append(('team_id', '=', self.team_id.id))
        consultation_stage = self.env['crm.stage'].search(domain, limit=1)
        if consultation_stage:
            self.stage_id = consultation_stage.id
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'res_id': event.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_convert_to_patient(self):
        """Convert inquiry to patient - KEY FUNCTION
        
        This function:
        1. Creates/updates res.partner
        2. Creates dental.patient (if clinic module installed)
        3. Creates dental.treatment (if clinic module installed)
        4. Links all records together
        5. Marks inquiry as won
        """
        self.ensure_one()
        
        # 1. Create/update partner
        if not self.partner_id:
            partner_vals = {
                'name': self.contact_name or self.name,
                'phone': self.phone,
                'email': self.email_from,
                'is_company': False,
            }
            # Add gender and date of birth if available
            if self.gender:
                # Map gender to Odoo's gender field if exists
                if hasattr(self.env['res.partner'], 'gender'):
                    gender_map = {
                        'male': 'male',
                        'female': 'female',
                        'other': 'other'
                    }
                    partner_vals['gender'] = gender_map.get(self.gender, False)
            if self.date_of_birth:
                if hasattr(self.env['res.partner'], 'date_of_birth'):
                    partner_vals['date_of_birth'] = self.date_of_birth
                elif hasattr(self.env['res.partner'], 'birthdate'):
                    partner_vals['birthdate'] = self.date_of_birth
            
            partner = self.env['res.partner'].create(partner_vals)
            self.partner_id = partner
        else:
            partner = self.partner_id
            # Update gender and date of birth if available
            update_vals = {}
            if self.gender and hasattr(partner, 'gender'):
                gender_map = {
                    'male': 'male',
                    'female': 'female',
                    'other': 'other'
                }
                update_vals['gender'] = gender_map.get(self.gender, False)
            if self.date_of_birth:
                if hasattr(partner, 'date_of_birth'):
                    update_vals['date_of_birth'] = self.date_of_birth
                elif hasattr(partner, 'birthdate'):
                    update_vals['birthdate'] = self.date_of_birth
            if update_vals:
                partner.write(update_vals)
        
        # Mark partner as dental patient (if field exists from integration module)
        if hasattr(partner, 'is_dental_patient'):
            partner.write({'is_dental_patient': True})
        
        # 2. Create dental.patient if clinic module exists
        dental_patient = False
        if 'dental.patient' in self.env:
            # Check if dental patient already exists for this partner
            # First check if partner has dental_patient_id field (from integration module)
            if hasattr(partner, 'dental_patient_id') and partner.dental_patient_id:
                dental_patient = partner.dental_patient_id
            else:
                # Search by phone or email
                domain = []
                if partner.phone:
                    domain.append(('phone', '=', partner.phone))
                elif partner.email:
                    domain.append(('email', '=', partner.email))
                
                if domain:
                    dental_patient = self.env['dental.patient'].search(domain, limit=1)
            
            # Create if not exists
            if not dental_patient:
                dental_patient_vals = {
                    'name': partner.name,
                    'phone': partner.phone,
                    'email': partner.email,
                    'address': partner.street or '',
                }
                # Add gender and date of birth if available
                if self.gender:
                    if hasattr(self.env['dental.patient'], 'gender'):
                        dental_patient_vals['gender'] = self.gender
                if self.date_of_birth:
                    if hasattr(self.env['dental.patient'], 'date_of_birth'):
                        dental_patient_vals['date_of_birth'] = self.date_of_birth
                    elif hasattr(self.env['dental.patient'], 'birthdate'):
                        dental_patient_vals['birthdate'] = self.date_of_birth
                
                dental_patient = self.env['dental.patient'].create(dental_patient_vals)
                
                # Link partner to dental patient (if integration module installed)
                if hasattr(partner, 'dental_patient_id'):
                    partner.write({'dental_patient_id': dental_patient.id})
            
            self.converted_dental_patient_id = dental_patient.id
            
            # 3. Create treatment case if clinic module exists
            if 'dental.treatment' in self.env:
                treatment = self.env['dental.treatment'].create({
                    'patient_id': dental_patient.id,
                    'treatment_type': self.treatment_interest or 'other',
                    'name': f"Điều trị từ Inquiry: {self.name}",
                    'status': 'information',
                    'total_cost': self.estimated_treatment_value or 0.0,
                    'notes': self.dental_issue or '',
                })
                self.treatment_case_id = treatment.id
                
                # Mark as won
                self.action_set_won()
                self.converted_patient_id = partner.id
                
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'dental.treatment',
                    'res_id': treatment.id,
                    'view_mode': 'form',
                    'target': 'current',
                }
            
            # Mark as won
            self.action_set_won()
            self.converted_patient_id = partner.id
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'dental.patient',
                'res_id': dental_patient.id,
                'view_mode': 'form',
                'target': 'current',
            }
        
        # 4. Mark as won (even if clinic module not installed)
        self.action_set_won()
        self.converted_patient_id = partner.id
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': partner.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Override to only show stages from dental inquiry team in kanban view
        
        This method is called by kanban view to determine which stages to display.
        We override it to ALWAYS return only the 4 stages from our dental inquiry team,
        excluding "Đã liên hệ" which has been removed.
        """
        # Get dental inquiry team
        dental_team = self.env['crm.team'].search([
            ('name', '=', 'Đội Inquiry Nha khoa')
        ], limit=1)
        
        if dental_team:
            # ALWAYS return only stages from dental team, ordered by sequence
            # Exclude "Đã liên hệ" stage explicitly
            # Note: Won stages (fold=True) should still be shown in kanban
            dental_stages = self.env['crm.stage'].search([
                ('team_id', '=', dental_team.id),
                ('name', '!=', 'Đã liên hệ'),  # Explicitly exclude removed stage
            ], order='sequence')
            return dental_stages
        
        # If team not found, return empty to avoid showing wrong stages
        return self.env['crm.stage']

