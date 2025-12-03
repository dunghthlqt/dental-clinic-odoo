# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class DentalPaymentPlan(models.Model):
    _name = 'dental.payment.plan'
    _description = 'Payment Plan for Dental Treatment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'upfront_payment_date desc'
    
    treatment_id = fields.Many2one(
        'dental.treatment',
        string='Điều trị',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    total_amount = fields.Float(
        'Tổng số tiền',
        related='treatment_id.total_cost',
        readonly=True,
        store=True
    )
    
    upfront_payment = fields.Float(
        'Đóng trước',
        compute='_compute_upfront',
        store=True,
        help='50% của tổng số tiền'
    )
    
    upfront_payment_date = fields.Date(
        'Ngày đóng trước',
        required=True,
        default=fields.Date.today,
        tracking=True,
        help='Ngày bắt đầu điều trị (ngày đóng 50%)'
    )
    
    installment_period = fields.Integer(
        'Số tháng trả góp',
        default=12,
        readonly=True,
        help='Số tháng trả góp (cố định 12 tháng)'
    )
    
    end_date = fields.Date(
        'Ngày kết thúc',
        compute='_compute_end_date',
        store=True,
        help='Ngày kết thúc kỳ trả góp (12 tháng từ ngày đóng trước)'
    )
    
    total_paid = fields.Float(
        'Đã thanh toán',
        compute='_compute_total_paid',
        store=True,
        help='Tổng số tiền đã thanh toán'
    )
    
    remaining_amount = fields.Float(
        'Còn lại',
        compute='_compute_remaining',
        store=True,
        help='Số tiền còn lại cần thanh toán'
    )
    
    is_overdue = fields.Boolean(
        'Quá hạn',
        compute='_compute_is_overdue',
        store=True,
        help='Quá hạn sau 12 tháng và còn nợ'
    )
    
    payment_ids = fields.One2many(
        'account.payment',
        'payment_plan_id',
        string='Payments',
        help='Các payments đã thực hiện'
    )
    
    payment_count = fields.Integer(
        'Số lần thanh toán',
        compute='_compute_payment_count'
    )
    
    @api.depends('total_amount')
    def _compute_upfront(self):
        """Tính 50% của tổng số tiền"""
        for plan in self:
            plan.upfront_payment = plan.total_amount * 0.5
    
    @api.depends('upfront_payment_date', 'installment_period')
    def _compute_end_date(self):
        """Tính ngày kết thúc: upfront_payment_date + 12 tháng"""
        for plan in self:
            if plan.upfront_payment_date:
                plan.end_date = plan.upfront_payment_date + relativedelta(months=plan.installment_period)
            else:
                plan.end_date = False
    
    @api.depends('payment_ids', 'payment_ids.state', 'payment_ids.amount')
    def _compute_total_paid(self):
        """Tính tổng số tiền đã thanh toán từ các payments đã posted"""
        for plan in self:
            posted_payments = plan.payment_ids.filtered(lambda p: p.state == 'posted')
            plan.total_paid = sum(posted_payments.mapped('amount'))
    
    @api.depends('total_amount', 'total_paid')
    def _compute_remaining(self):
        """Tính số tiền còn lại"""
        for plan in self:
            plan.remaining_amount = plan.total_amount - plan.total_paid
    
    @api.depends('end_date', 'remaining_amount')
    def _compute_is_overdue(self):
        """Kiểm tra quá hạn: Sau 12 tháng và còn nợ"""
        today = fields.Date.today()
        for plan in self:
            if plan.end_date and plan.end_date < today:
                plan.is_overdue = plan.remaining_amount > 0
            else:
                plan.is_overdue = False
    
    def _compute_payment_count(self):
        """Đếm số lần thanh toán"""
        for plan in self:
            plan.payment_count = len(plan.payment_ids)
    
    @api.constrains('upfront_payment', 'total_amount')
    def _check_upfront_payment(self):
        """Kiểm tra upfront_payment = 50% của total_amount"""
        for plan in self:
            if plan.total_amount > 0:
                expected_upfront = plan.total_amount * 0.5
                if abs(plan.upfront_payment - expected_upfront) > 0.01:
                    raise ValidationError(
                        f'Đóng trước phải bằng 50% của tổng số tiền. '
                        f'Hiện tại: {plan.upfront_payment}, Mong đợi: {expected_upfront}'
                    )
    
    @api.constrains('installment_period')
    def _check_installment_period(self):
        """Kiểm tra installment_period = 12 (cố định)"""
        for plan in self:
            if plan.installment_period != 12:
                raise ValidationError('Số tháng trả góp phải là 12 tháng (cố định)')
    
    def action_view_payments(self):
        """Mở view payments của payment plan"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('payment_plan_id', '=', self.id)],
            'context': {'default_payment_plan_id': self.id},
        }
    
    def action_view_invoices(self):
        """Mở view invoices liên quan đến payment plan"""
        self.ensure_one()
        invoices = self.env['account.move'].search([
            ('dental_treatment_id', '=', self.treatment_id.id),
            ('move_type', 'in', ['out_invoice', 'out_receipt'])
        ])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', invoices.ids)],
        }

