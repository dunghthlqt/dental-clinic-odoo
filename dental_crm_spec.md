# Dental CRM Module - Technical Specification

## 1. Overview

**Module Name**: `dental_inquiry`  
**Odoo Version**: 17.0  
**Purpose**: Simplified Healthcare CRM for dental clinics - Manage patient inquiries from initial contact to conversion

**Key Principle**: EXTEND Odoo CRM (`crm.lead`), DO NOT create new models from scratch.

---

## 2. Architecture & Strategy

### 2.1 Core Concept

```
PRE-PATIENT (CRM manages) → CONVERSION → POST-PATIENT (Clinic manages)

Inquiry → Consultation → Decision → [Convert] → Patient → Treatment
  ↑                                                ↑
  CRM Module                                      Clinic Module
```

### 2.2 What CRM Does vs Does NOT Do

**CRM Manages:**
- Inquiry capture (phone, Facebook, website)
- Consultation scheduling (sales-oriented)
- Follow-up tracking for undecided customers
- Conversion to patient

**CRM Does NOT Manage:**
- Clinical treatment records
- Treatment sessions
- Medical history details
- Billing/invoicing

**Handoff Point**: When customer agrees to treatment → Convert to Patient → Clinic module takes over

---

## 3. Data Models

### 3.1 Extend `crm.lead`

```python
# models/crm_lead.py

from odoo import models, fields, api
from datetime import timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    # Dental-specific inquiry info
    dental_issue = fields.Text(string='Dental Issue Description')
    treatment_interest = fields.Selection([
        ('orthodontics', 'Niềng răng'),
        ('implant', 'Cấy ghép Implant'),
        ('root_canal', 'Điều trị tủy'),
        ('extraction', 'Nhổ răng'),
        ('restoration', 'Hàn trám'),
        ('cleaning', 'Vệ sinh răng'),
        ('whitening', 'Tẩy trắng'),
        ('other', 'Khác')
    ], string='Treatment Interest')
    
    urgency_level = fields.Selection([
        ('low', 'Không gấp'),
        ('medium', 'Bình thường'),
        ('high', 'Gấp'),
        ('emergency', 'Cấp cứu')
    ], string='Urgency', default='medium')
    
    # Consultation tracking
    consultation_date = fields.Datetime(string='Consultation Scheduled')
    consultation_event_id = fields.Many2one('calendar.event', string='Consultation Appointment', readonly=True)
    consultation_notes = fields.Text(string='Consultation Notes')
    estimated_treatment_value = fields.Float(string='Estimated Treatment Cost')
    
    # Conversion tracking
    converted_patient_id = fields.Many2one('res.partner', string='Converted to Patient', readonly=True)
    converted_dental_patient_id = fields.Many2one('dental.patient', string='Converted Dental Patient', readonly=True)
    treatment_case_id = fields.Many2one('dental.treatment', string='Treatment Case', readonly=True)
    
    # Computed
    is_high_value = fields.Boolean(compute='_compute_is_high_value', store=True)
    
    @api.depends('estimated_treatment_value')
    def _compute_is_high_value(self):
        for lead in self:
            lead.is_high_value = lead.estimated_treatment_value >= 20000000
    
    @api.onchange('estimated_treatment_value')
    def _onchange_estimated_treatment_value(self):
        if self.estimated_treatment_value:
            self.expected_revenue = self.estimated_treatment_value
    
    def action_schedule_consultation(self):
        """Create consultation appointment"""
        self.ensure_one()
        event = self.env['calendar.event'].create({
            'name': f'Consultation: {self.contact_name or self.name}',
            'start': self.consultation_date or fields.Datetime.now(),
            'stop': (self.consultation_date or fields.Datetime.now()) + timedelta(hours=1),
            'partner_ids': [(4, self.partner_id.id)] if self.partner_id else [],
            'lead_id': self.id,
            'appointment_type': 'consultation',
        })
        self.consultation_event_id = event.id
        return {'type': 'ir.actions.act_window', 'res_model': 'calendar.event', 'res_id': event.id, 'view_mode': 'form'}
    
    def action_convert_to_patient(self):
        """Convert inquiry to patient - KEY FUNCTION"""
        self.ensure_one()
        
        # Create/update partner
        if not self.partner_id:
            partner = self.env['res.partner'].create({
                'name': self.contact_name or self.name,
                'phone': self.phone,
                'email': self.email_from,
                'is_dental_patient': True,
            })
            self.partner_id = partner
        else:
            self.partner_id.write({'is_dental_patient': True})
        
        # Mark as won
        self.action_set_won()
        self.converted_patient_id = self.partner_id.id
        
        # Create dental.patient if clinic module exists
        dental_patient = False
        if 'dental.patient' in self.env:
            # Check if dental patient already exists for this partner
            dental_patient = self.env['dental.patient'].search([
                ('partner_id', '=', self.partner_id.id)
            ], limit=1)
            
            if not dental_patient:
                dental_patient = self.env['dental.patient'].create({
                    'name': self.partner_id.name,
                    'phone': self.partner_id.phone,
                    'email': self.partner_id.email,
                    'address': self.partner_id.street or '',
                    'partner_id': self.partner_id.id,
                })
            
            self.converted_dental_patient_id = dental_patient.id
            
            # Create treatment case if clinic module exists
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
                return {'type': 'ir.actions.act_window', 'res_model': 'dental.treatment', 'res_id': treatment.id, 'view_mode': 'form'}
            
            return {'type': 'ir.actions.act_window', 'res_model': 'dental.patient', 'res_id': dental_patient.id, 'view_mode': 'form'}
        
        return {'type': 'ir.actions.act_window', 'res_model': 'res.partner', 'res_id': self.partner_id.id, 'view_mode': 'form'}
```

### 3.2 Extend `calendar.event`

```python
# models/calendar_event.py

from odoo import models, fields, api

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'
    
    appointment_type = fields.Selection([
        ('consultation', 'Consultation (Sales)'),
        ('treatment', 'Treatment Session'),
        ('followup', 'Follow-up Check'),
        ('emergency', 'Emergency'),
        ('other', 'Other')
    ], string='Appointment Type', default='other')
    
    lead_id = fields.Many2one('crm.lead', string='Related Inquiry')
    treatment_session_id = fields.Many2one('treatment.session', string='Treatment Session')
    
    patient_id = fields.Many2one('res.partner', string='Patient', compute='_compute_patient', store=True)
    
    @api.depends('lead_id', 'treatment_session_id', 'partner_ids')
    def _compute_patient(self):
        for event in self:
            if event.treatment_session_id:
                event.patient_id = event.treatment_session_id.patient_id
            elif event.lead_id:
                event.patient_id = event.lead_id.partner_id
            elif event.partner_ids:
                event.patient_id = event.partner_ids[0]
            else:
                event.patient_id = False
```

### 3.3 Extend `res.partner` (Minimal)

```python
# models/res_partner.py

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_dental_patient = fields.Boolean(string='Is Dental Patient', default=False)
    inquiry_ids = fields.One2many('crm.lead', 'partner_id', string='Inquiries')
```

---

## 4. Views

### 4.1 Extend CRM Lead Form

```xml
<!-- views/crm_lead_views.xml -->
<record id="view_crm_lead_form_dental" model="ir.ui.view">
    <field name="name">crm.lead.form.dental</field>
    <field name="model">crm.lead</field>
    <field name="inherit_id" ref="crm.crm_lead_view_form"/>
    <field name="arch" type="xml">
        
        <!-- Add buttons in header -->
        <xpath expr="//header" position="inside">
            <button name="action_schedule_consultation" string="Schedule Consultation" type="object" class="btn-primary"
                    invisible="consultation_event_id or type != 'lead'"/>
            <button name="action_convert_to_patient" string="Convert to Patient" type="object" class="btn-success"
                    invisible="stage_id.is_won or not partner_id"/>
        </xpath>
        
        <!-- Add Dental Information tab -->
        <xpath expr="//notebook" position="inside">
            <page string="Dental Information">
                <group>
                    <group>
                        <field name="dental_issue"/>
                        <field name="treatment_interest"/>
                        <field name="urgency_level"/>
                    </group>
                    <group>
                        <field name="consultation_date"/>
                        <field name="consultation_event_id" readonly="1"/>
                        <field name="estimated_treatment_value"/>
                        <field name="consultation_notes"/>
                    </group>
                </group>
            </page>
        </xpath>
        
        <xpath expr="//sheet" position="before">
            <field name="is_high_value" invisible="1"/>
        </xpath>
        
    </field>
</record>
```

### 4.2 Menu Structure (Use dental terminology, not "CRM")

```xml
<!-- views/inquiry_menus.xml -->
<menuitem id="menu_dental_inquiries_root" name="Patient Inquiries" sequence="5"/>

<record id="action_dental_inquiries" model="ir.actions.act_window">
    <field name="name">Inquiries</field>
    <field name="res_model">crm.lead</field>
    <field name="view_mode">kanban,tree,form,calendar,graph,pivot</field>
    <field name="domain">[('type', '=', 'lead')]</field>
    <field name="context">{'default_type': 'lead', 'search_default_open': 1}</field>
</record>

<menuitem id="menu_dental_inquiries" name="All Inquiries" parent="menu_dental_inquiries_root" action="action_dental_inquiries"/>

<record id="action_consultation_calendar" model="ir.actions.act_window">
    <field name="name">Consultation Calendar</field>
    <field name="res_model">calendar.event</field>
    <field name="view_mode">calendar,tree,form</field>
    <field name="domain">[('appointment_type', '=', 'consultation')]</field>
    <field name="context">{'default_appointment_type': 'consultation'}</field>
</record>

<menuitem id="menu_consultation_calendar" name="Calendar" parent="menu_dental_inquiries_root" action="action_consultation_calendar"/>
```

---

## 5. Security

### 5.1 Groups

```xml
<!-- security/dental_security.xml -->
<record id="module_category_dental_inquiry" model="ir.module.category">
    <field name="name">Patient Inquiry Management</field>
</record>

<record id="group_dental_receptionist" model="res.groups">
    <field name="name">Receptionist</field>
    <field name="category_id" ref="module_category_dental_inquiry"/>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>

<record id="group_dental_dentist" model="res.groups">
    <field name="name">Dentist</field>
    <field name="category_id" ref="module_category_dental_inquiry"/>
    <field name="implied_ids" eval="[(4, ref('group_dental_receptionist'))]"/>
</record>

<record id="group_dental_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="category_id" ref="module_category_dental_inquiry"/>
    <field name="implied_ids" eval="[(4, ref('group_dental_dentist'))]"/>
</record>
```

### 5.2 Access Rights

```csv
# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_crm_lead_receptionist,crm.lead.receptionist,crm.model_crm_lead,group_dental_receptionist,1,1,1,0
access_crm_lead_dentist,crm.lead.dentist,crm.model_crm_lead,group_dental_dentist,1,1,0,0
access_crm_lead_manager,crm.lead.manager,crm.model_crm_lead,group_dental_manager,1,1,1,1
```

### 5.3 Record Rules

```xml
<!-- security/dental_record_rules.xml -->
<record id="rule_inquiry_receptionist_all" model="ir.rule">
    <field name="name">Receptionist: All Inquiries</field>
    <field name="model_id" ref="crm.model_crm_lead"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('group_dental_receptionist'))]"/>
</record>

<record id="rule_inquiry_dentist_own" model="ir.rule">
    <field name="name">Dentist: Own Inquiries</field>
    <field name="model_id" ref="crm.model_crm_lead"/>
    <field name="domain_force">['|', ('user_id', '=', user.id), ('user_id', '=', False)]</field>
    <field name="groups" eval="[(4, ref('group_dental_dentist'))]"/>
</record>
```

---

## 6. CRM Stages

```xml
<!-- data/crm_stage_data.xml -->
<record id="stage_new_inquiry" model="crm.stage">
    <field name="name">New Inquiry</field>
    <field name="sequence">1</field>
</record>

<record id="stage_contacted" model="crm.stage">
    <field name="name">Contacted</field>
    <field name="sequence">2</field>
</record>

<record id="stage_consultation_scheduled" model="crm.stage">
    <field name="name">Consultation Scheduled</field>
    <field name="sequence">3</field>
</record>

<record id="stage_consulted_pending" model="crm.stage">
    <field name="name">Consulted - Pending</field>
    <field name="sequence">4</field>
</record>

<record id="stage_won" model="crm.stage">
    <field name="name">Patient Acquired</field>
    <field name="sequence">5</field>
    <field name="is_won" eval="True"/>
    <field name="fold" eval="True"/>
</record>
```

---

## 7. Manifest

```python
# __manifest__.py
{
    'name': 'Dental Patient Inquiry Management',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/CRM',
    'summary': 'Simplified CRM for dental clinic',
    'depends': ['base', 'crm', 'calendar', 'contacts'],
    'data': [
        'security/dental_security.xml',
        'security/ir.model.access.csv',
        'security/dental_record_rules.xml',
        'data/crm_stage_data.xml',
        'views/crm_lead_views.xml',
        'views/calendar_event_views.xml',
        'views/res_partner_views.xml',
        'views/inquiry_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

---

## 8. Workflow Examples

### Workflow 1: Online Inquiry → Consultation → Convert
```
1. Customer messages on Facebook: "Want to ask about braces"
   → Receptionist creates inquiry (crm.lead)
   → Fields: dental_issue="Crooked teeth", treatment_interest="orthodontics"

2. Receptionist calls customer
   → Updates stage to "Contacted"
   → Adds activity note

3. Customer agrees to consultation
   → Click "Schedule Consultation" button
   → System creates calendar.event with appointment_type='consultation'
   → Stage changes to "Consultation Scheduled"

4. Customer visits, dentist consults
   → Dentist adds: consultation_notes, estimated_treatment_value
   → Stage: "Consulted - Pending"

5. Customer decides
   A) Agrees → Click "Convert to Patient"
      → Creates/updates res.partner (is_dental_patient=True)
      → Creates dental.treatment.case (if clinic module installed)
      → Stage: Won
   
   B) Needs time → Set follow-up activity (call in 3 days)
   
   C) Declines → Mark as Lost with reason
```

### Workflow 2: Walk-in (Skip CRM)
```
Customer walks in ready for treatment
→ NO inquiry needed
→ Receptionist creates res.partner directly
→ Goes straight to Clinic module
```

---

## 9. Key Differences

### CRM vs Clinic

| Aspect | CRM (Inquiry) | Clinic (Treatment) |
|--------|---------------|-------------------|
| **Purpose** | Convert inquiries to patients | Manage clinical treatment |
| **User** | Receptionist, Sales | Dentist, Clinical staff |
| **Data** | Contact info, inquiry details | Medical history, treatment records |
| **Appointment** | Consultation (sales) | Treatment sessions |
| **Outcome** | Won/Lost | Treatment completed |

### Consultation vs Treatment Appointment

```python
# Consultation (CRM context)
calendar.event {
    appointment_type: 'consultation',
    lead_id: <crm.lead>,        # Links to inquiry
    # Purpose: Initial assessment, price quote, close deal
}

# Treatment (Clinic context)
calendar.event {
    appointment_type: 'treatment',
    treatment_session_id: <dental.treatment.session>,  # Links to clinical record
    # Purpose: Actual dental procedure
}
```

---

## 10. Critical Rules

### DO's ✅
- Extend `crm.lead`, don't create new models
- Use `appointment_type` to differentiate consultation vs treatment
- Always capture lost reasons
- Keep CRM lightweight (no clinical data)
- Use dental terminology in UI ("Inquiry" not "Lead")

### DON'Ts ❌
- Don't add clinical fields to CRM (tooth_number, x-rays, etc.)
- Don't mix inquiry and patient records
- Don't use CRM for treatment management
- Don't skip the conversion step (always click "Convert to Patient")
- Don't create patients directly when inquiry comes in (create lead first)

---

## 11. Integration Points

### With Clinic Module
```python
# CRM provides to Clinic:
- Basic patient info (name, phone, email)
- Inquiry source tracking
- Initial dental issue
- Treatment interest
- Estimated budget

# Clinic provides back to CRM:
- Treatment case ID (for tracking)
- Conversion confirmation
```

### With Calendar Module
```python
# CRM creates consultation appointments
# Clinic creates treatment appointments
# Both use calendar.event but with different appointment_type
```

---

## 12. Testing Checklist

- [ ] Create inquiry from scratch
- [ ] Schedule consultation appointment
- [ ] Add consultation notes as dentist
- [ ] Convert to patient successfully
- [ ] Verify patient record created
- [ ] Verify treatment case created (if clinic module)
- [ ] Mark inquiry as lost with reason
- [ ] Test access rights (receptionist, dentist, manager)
- [ ] Test duplicate detection (same phone/email)
- [ ] Verify conversion metrics in reports

---

## 13. Notes for AI Coding Agent

**Implementation Priority:**
1. Models first (crm_lead, calendar_event, res_partner)
2. Key functions (action_schedule_consultation, action_convert_to_patient)
3. Views (form inherit, menu)
4. Security (groups, access rights, record rules)
5. Data (stages)

**Code Style:**
- Follow Odoo conventions
- Use `self.ensure_one()` for singleton methods
- Add proper help text to fields
- Use `readonly=True` for computed/system fields
- Add docstrings to methods

**Common Pitfalls:**
- Don't forget `__init__.py` in models/
- Security files must be loaded before views in manifest
- Use `ref()` for XML IDs in eval context
- Test with both clinic module installed and not installed

**File Structure:**
```
dental_inquiry/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── crm_lead.py
│   ├── calendar_event.py
│   └── res_partner.py
├── views/
│   ├── crm_lead_views.xml
│   ├── calendar_event_views.xml
│   ├── res_partner_views.xml
│   └── inquiry_menus.xml
├── security/
│   ├── dental_security.xml
│   ├── ir.model.access.csv
│   └── dental_record_rules.xml
└── data/
    └── crm_stage_data.xml
```

End of specification.