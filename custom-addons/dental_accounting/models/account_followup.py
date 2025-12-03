# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import fields, models, api


class AccountFollowup(models.Model):
    """Account Follow-up for Dental Clinic
    
    Independent implementation for dental clinic accounting.
    Manages follow-up actions for overdue payments on installment treatments.
    """
    _name = 'account.followup'
    _description = 'Account Follow-up'
    _rec_name = 'name'
    _order = 'company_id'

    followup_line_ids = fields.One2many(
        'followup.line',
        'followup_id',
        'Follow-up',
        copy=True
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.company,
        required=True,
        readonly=True
    )
    name = fields.Char(
        related='company_id.name',
        readonly=True,
        store=True
    )
    
    @api.model
    def default_get(self, fields_list):
        """Set default company"""
        res = super().default_get(fields_list)
        if 'company_id' not in res:
            res['company_id'] = self.env.company.id
        return res


class FollowupLine(models.Model):
    """Follow-up Criteria for Dental Clinic
    
    Defines follow-up actions based on overdue days for installment treatments.
    """
    _name = 'followup.line'
    _description = 'Follow-up Criteria'
    _order = 'delay'

    name = fields.Char(
        'Follow-Up Action',
        required=True,
        translate=True
    )
    sequence = fields.Integer(
        help="Gives the sequence order when displaying a list of follow-up lines."
    )
    delay = fields.Integer(
        'Due Days',
        required=True,
        help="The number of days after the due date of the invoice "
             "to wait before sending the reminder. "
             "Could be negative if you want to send a polite alert beforehand."
    )
    followup_id = fields.Many2one(
        'account.followup',
        'Follow Ups',
        required=True,
        ondelete="cascade"
    )
    
    @api.model
    def default_get(self, fields_list):
        """Set default followup_id from context"""
        res = super().default_get(fields_list)
        # Nếu có followup_id trong context (khi tạo từ tree view)
        if 'default_followup_id' in self.env.context:
            res['followup_id'] = self.env.context.get('default_followup_id')
        # Nếu không có, tìm followup của company hiện tại
        elif 'followup_id' not in res:
            followup = self.env['account.followup'].search([
                ('company_id', '=', self.env.company.id)
            ], limit=1)
            if followup:
                res['followup_id'] = followup.id
        return res


class ResPartner(models.Model):
    """Extend res.partner with follow-up fields - Customized for dental"""
    _inherit = "res.partner"

    invoice_list = fields.One2many(
        'account.move',
        'partner_id',
        string="Invoice Details",
        readonly=True,
        domain=[
            ('payment_state', '=', 'not_paid'),
            ('move_type', '=', 'out_invoice'),
            # Customize: Chỉ hiển thị invoices từ installment treatments
            # Note: Domain với related fields có thể không hoạt động, sẽ filter trong computed method
            ('dental_treatment_id', '!=', False),
        ]
    )
    
    total_due = fields.Monetary(
        compute='_compute_for_followup',
        store=False,
        readonly=True,
        currency_field='currency_id'
    )
    
    next_reminder_date = fields.Date(
        compute='_compute_for_followup',
        store=False,
        readonly=True
    )
    
    total_overdue = fields.Monetary(
        compute='_compute_for_followup',
        store=False,
        readonly=True,
        currency_field='currency_id'
    )
    
    followup_status = fields.Selection(
        [
            ('in_need_of_action', 'In need of action'),
            ('with_overdue_invoices', 'With overdue invoices'),
            ('no_action_needed', 'No action needed')
        ],
        string='Followup status',
        compute='_compute_for_followup',
        store=False,
        readonly=True
    )

    def _compute_for_followup(self):
        """
        Compute the fields 'total_due', 'total_overdue',
        'next_reminder_date' and 'followup_status'
        Customized: Chỉ tính cho invoices từ installment treatments sau 12 tháng
        """
        for record in self:
            total_due = 0
            total_overdue = 0
            today = fields.Date.today()
            
            # Filter invoices: chỉ installment treatments và overdue
            dental_invoices = record.invoice_list.filtered(
                lambda inv: inv.dental_treatment_id and
                inv.dental_treatment_id.payment_policy == 'installment' and
                inv.dental_treatment_id.payment_plan_id and
                inv.dental_treatment_id.payment_plan_id.is_overdue
            )
            
            for am in dental_invoices:
                if am.company_id == self.env.company:
                    amount = am.amount_residual
                    total_due += amount

                    is_overdue = today > am.invoice_date_due \
                        if am.invoice_date_due else today > am.date
                    if is_overdue:
                        total_overdue += amount or 0
            
            min_date = record.get_min_date()
            action = record.action_after()
            
            if min_date:
                date_reminder = min_date + timedelta(days=action)
                if date_reminder:
                    record.next_reminder_date = date_reminder
            else:
                date_reminder = today
                record.next_reminder_date = date_reminder
            
            if total_overdue > 0 and date_reminder > today:
                followup_status = "with_overdue_invoices"
            elif total_due > 0 and date_reminder <= today:
                followup_status = "in_need_of_action"
            else:
                followup_status = "no_action_needed"
            
            record.total_due = total_due
            record.total_overdue = total_overdue
            record.followup_status = followup_status

    def get_min_date(self):
        """Get minimum due date from invoices"""
        today = date.today()
        for this in self:
            if this.invoice_list:
                # Filter dental invoices only
                dental_invoices = this.invoice_list.filtered(
                    lambda inv: inv.dental_treatment_id and
                    inv.dental_treatment_id.payment_policy == 'installment'
                )
                if dental_invoices:
                    min_list = dental_invoices.mapped('invoice_date_due')
                    while False in min_list:
                        min_list.remove(False)
                    if min_list:
                        return min(min_list)
            return today

    def get_delay(self):
        """Get follow-up delay from database"""
        delay = """SELECT fl.id, fl.delay
                    FROM followup_line fl
                    JOIN account_followup af ON fl.followup_id = af.id
                    WHERE af.company_id = %s
                    ORDER BY fl.delay;
                    """
        self._cr.execute(delay, [self.env.company.id])
        record = self._cr.dictfetchall()
        return record

    def action_after(self):
        """Get action delay"""
        lines = self.env['followup.line'].search([
            ('followup_id.company_id', '=', self.env.company.id)
        ])
        if lines:
            record = self.get_delay()
            for i in record:
                return i['delay']
        return 0

