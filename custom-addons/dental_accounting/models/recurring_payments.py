# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class FilterRecurringEntries(models.Model):
    """Extend account.move with recurring reference field"""
    _inherit = 'account.move'
    
    recurring_ref = fields.Char(
        string='Recurring Ref',
        help='Reference to recurring payment template'
    )


class RecurringPayments(models.Model):
    """Recurring Payments for fixed costs - Copy & Adapt from base_accounting_kit"""
    _name = 'account.recurring.payments'
    _description = 'Accounting Recurring Payment'

    @api.depends('date', 'recurring_period', 'recurring_interval')
    def _get_next_schedule(self):
        """Function for adding the schedule process"""
        for record in self:
            if record.date:
                recurr_dates = []
                today = datetime.today()
                start_date = datetime.strptime(str(record.date), '%Y-%m-%d')
                while start_date <= today:
                    recurr_dates.append(str(start_date.date()))
                    if record.recurring_period == 'days':
                        start_date += relativedelta(days=record.recurring_interval)
                    elif record.recurring_period == 'weeks':
                        start_date += relativedelta(weeks=record.recurring_interval)
                    elif record.recurring_period == 'months':
                        start_date += relativedelta(months=record.recurring_interval)
                    else:
                        start_date += relativedelta(years=record.recurring_interval)
                record.next_date = start_date.date()
            else:
                record.next_date = False

    name = fields.Char(string='Tên', required=True)
    debit_account = fields.Many2one(
        'account.account',
        'Tài khoản Nợ',
        required=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
    credit_account = fields.Many2one(
        'account.account',
        'Tài khoản Có',
        required=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
    journal_id = fields.Many2one(
        'account.journal',
        'Sổ nhật ký',
        required=True
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Tài khoản phân tích'
    )
    date = fields.Date(
        'Ngày bắt đầu',
        required=True,
        default=date.today()
    )
    next_date = fields.Date(
        'Ngày tiếp theo',
        compute='_get_next_schedule',
        store=True,
        readonly=True,
        copy=False
    )
    recurring_period = fields.Selection(
        selection=[
            ('days', 'Ngày'),
            ('weeks', 'Tuần'),
            ('months', 'Tháng'),
            ('years', 'Năm')
        ],
        store=True,
        required=True,
        string='Chu kỳ'
    )
    amount = fields.Float('Số tiền', required=True)
    description = fields.Text('Mô tả')
    state = fields.Selection(
        selection=[
            ('draft', 'Nháp'),
            ('running', 'Đang chạy')
        ],
        default='draft',
        string='Trạng thái'
    )
    journal_state = fields.Selection(
        selection=[
            ('draft', 'Chưa đăng'),
            ('posted', 'Đã đăng')
        ],
        required=True,
        default='draft',
        string='Tạo bút toán dạng'
    )
    recurring_interval = fields.Integer('Khoảng cách', default=1)
    partner_id = fields.Many2one('res.partner', 'Đối tác')
    pay_time = fields.Selection(
        selection=[
            ('pay_now', 'Thanh toán ngay'),
            ('pay_later', 'Thanh toán sau')
        ],
        store=True,
        required=True,
        string='Thời điểm thanh toán'
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda l: l.env.company.id
    )
    recurring_lines = fields.One2many(
        'account.recurring.entries.line',
        'tmpl_id'
    )
    
    def action_start_recurring(self):
        """Start recurring payment"""
        self.write({'state': 'running'})
    
    def action_stop_recurring(self):
        """Stop recurring payment"""
        self.write({'state': 'draft'})

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """Onchange partner field for updating the credit account value"""
        if self.partner_id and self.partner_id.property_account_receivable_id:
            self.credit_account = self.partner_id.property_account_receivable_id

    @api.model
    def _cron_generate_entries(self):
        """Cron job to automatically generate recurring entries"""
        data = self.env['account.recurring.payments'].search([
            ('state', '=', 'running')
        ])
        entries = self.env['account.move'].search([
            ('recurring_ref', '!=', False)
        ])
        journal_dates = []
        journal_codes = []
        remaining_dates = []
        
        for entry in entries:
            journal_dates.append(str(entry.date))
            if entry.recurring_ref:
                journal_codes.append(str(entry.recurring_ref))
        
        today = datetime.today()
        for line in data:
            if line.date:
                recurr_dates = []
                start_date = datetime.strptime(str(line.date), '%Y-%m-%d')
                while start_date <= today:
                    recurr_dates.append(str(start_date.date()))
                    if line.recurring_period == 'days':
                        start_date += relativedelta(days=line.recurring_interval)
                    elif line.recurring_period == 'weeks':
                        start_date += relativedelta(weeks=line.recurring_interval)
                    elif line.recurring_period == 'months':
                        start_date += relativedelta(months=line.recurring_interval)
                    else:
                        start_date += relativedelta(years=line.recurring_interval)
                
                for rec in recurr_dates:
                    recurr_code = str(line.id) + '/' + str(rec)
                    if recurr_code not in journal_codes:
                        remaining_dates.append({
                            'date': rec,
                            'template_name': line.name,
                            'amount': line.amount,
                            'tmpl_id': line.id,
                        })
        
        child_ids = self.env['account.recurring.entries.line'].create(remaining_dates)
        for line in child_ids:
            tmpl_id = line.tmpl_id
            recurr_code = str(tmpl_id.id) + '/' + str(line.date)
            line_ids = [
                (0, 0, {
                    'account_id': tmpl_id.credit_account.id,
                    'partner_id': tmpl_id.partner_id.id if tmpl_id.partner_id else False,
                    'credit': line.amount,
                    'analytic_account_id': tmpl_id.analytic_account_id.id if tmpl_id.analytic_account_id else False,
                }),
                (0, 0, {
                    'account_id': tmpl_id.debit_account.id,
                    'partner_id': tmpl_id.partner_id.id if tmpl_id.partner_id else False,
                    'debit': line.amount,
                    'analytic_account_id': tmpl_id.analytic_account_id.id if tmpl_id.analytic_account_id else False,
                })
            ]
            vals = {
                'date': line.date,
                'recurring_ref': recurr_code,
                'company_id': self.env.company.id,
                'journal_id': tmpl_id.journal_id.id,
                'ref': line.template_name,
                'narration': 'Recurring entry',
                'line_ids': line_ids
            }
            move_id = self.env['account.move'].create(vals)
            if tmpl_id.journal_state == 'posted':
                move_id.action_post()


class GetAllRecurringEntries(models.TransientModel):
    """Account Recurring Entries Line"""
    _name = 'account.recurring.entries.line'
    _description = 'Account Recurring Entries Line'

    date = fields.Date('Ngày')
    template_name = fields.Char('Tên mẫu')
    amount = fields.Float('Số tiền')
    tmpl_id = fields.Many2one(
        'account.recurring.payments',
        string='Mẫu'
    )

