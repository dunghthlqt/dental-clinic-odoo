# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    dental_treatment_id = fields.Many2one(
        'dental.treatment',
        string='Điều trị liên quan',
        help='Điều trị liên quan đến payment này'
    )
    
    payment_plan_id = fields.Many2one(
        'dental.payment.plan',
        string='Payment Plan',
        help='Payment Plan liên quan (nếu có)'
    )
    
    auto_create_invoice = fields.Boolean(
        'Tự động tạo hóa đơn',
        default=True,
        help='Tự động tạo invoice sau khi payment được posted'
    )
    
    @api.onchange('dental_treatment_id')
    def _onchange_dental_treatment_id(self):
        """Auto-fill payment_plan_id và partner_id từ treatment"""
        if self.dental_treatment_id:
            # Set payment plan nếu có
            if self.dental_treatment_id.payment_plan_id:
                self.payment_plan_id = self.dental_treatment_id.payment_plan_id.id
            
            # Set partner từ patient
            if self.dental_treatment_id.patient_id:
                # Tìm partner từ dental patient
                partner = self.env['res.partner'].search([
                    ('phone', '=', self.dental_treatment_id.patient_id.phone)
                ], limit=1)
                if partner:
                    self.partner_id = partner.id
                else:
                    # Nếu chưa có partner, tạo mới
                    partner = self.env['res.partner'].create({
                        'name': self.dental_treatment_id.patient_id.name,
                        'phone': self.dental_treatment_id.patient_id.phone,
                        'email': self.dental_treatment_id.patient_id.email,
                    })
                    self.partner_id = partner.id
            
            # Set payment_type = 'inbound' (nhận tiền từ khách hàng)
            if not self.payment_type:
                self.payment_type = 'inbound'
    
    @api.constrains('amount', 'dental_treatment_id')
    def _check_payment_amount(self):
        """Kiểm tra payment amount không vượt quá remaining amount"""
        for payment in self:
            if payment.dental_treatment_id and payment.state != 'posted':
                treatment = payment.dental_treatment_id
                remaining = treatment.total_cost - treatment.revenue
                
                if payment.amount > remaining:
                    raise ValidationError(
                        f'Số tiền thanh toán ({payment.amount:,.0f}) '
                        f'vượt quá số tiền còn lại ({remaining:,.0f})'
                    )
    
    def action_post(self):
        """Override: Tạo invoice tự động sau khi payment được posted"""
        result = super().action_post()

        for payment in self:
            if payment.auto_create_invoice and payment.dental_treatment_id:
                # Tạo invoice từ payment
                invoice = payment._create_invoice_from_payment()
                if invoice:
                    # Link invoice với payment (nếu có field invoice_ids)
                    if hasattr(payment, 'invoice_ids'):
                        payment.invoice_ids = [(4, invoice.id)]
                
                # Invalidate cache để trigger recompute của revenue và payment_status
                payment.dental_treatment_id._compute_revenue()
                payment.dental_treatment_id._compute_payment_status_and_paid_amount()

        return result
    
    def _create_invoice_from_payment(self):
        """Tạo invoice từ payment (proof of payment)"""
        self.ensure_one()
        
        if not self.partner_id:
            raise UserError('Cần chọn Partner để tạo invoice')
        
        if not self.dental_treatment_id:
            raise UserError('Cần chọn Treatment để tạo invoice')
        
        # Tìm hoặc tạo product dịch vụ nha khoa
        product = self.env['product.product'].search([
            ('name', 'ilike', 'Dịch vụ nha khoa')
        ], limit=1)
        
        if not product:
            # Tạo product mặc định nếu chưa có (hoặc dùng service product có sẵn)
            product = self.env['product.product'].search([
                ('type', '=', 'service'),
                ('sale_ok', '=', True)
            ], limit=1)
            
            if not product:
                # Tạo product mới nếu không tìm thấy
                product = self.env['product.product'].create({
                    'name': 'Dịch vụ nha khoa',
                    'type': 'service',
                    'sale_ok': True,
                })
        
        # Tạo invoice
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': self.date,
            'date': self.date,
            'dental_treatment_id': self.dental_treatment_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'name': f'Thanh toán điều trị: {self.dental_treatment_id.name}',
                'quantity': 1,
                'price_unit': self.amount,
                'tax_ids': [(5, 0, 0)],  # Xóa tất cả thuế (không áp dụng thuế)
            })],
        }
        
        invoice = self.env['account.move'].create(invoice_vals)
        
        # Post invoice ngay (vì đã nhận tiền)
        if invoice.state == 'draft':
            invoice.action_post()
        
        # Reconcile payment với invoice để cập nhật trạng thái thanh toán
        self._reconcile_payment_with_invoice(invoice)
        
        return invoice
    
    def _reconcile_payment_with_invoice(self, invoice):
        """Reconcile payment với invoice để cập nhật trạng thái thanh toán"""
        self.ensure_one()
        
        if not invoice or invoice.state != 'posted':
            return
        
        # Tìm các move lines cần reconcile
        # Payment line (receivable account) - Odoo 17 sử dụng account_type thay vì internal_type
        payment_lines = self.line_ids.filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled
        )
        
        # Invoice line (receivable account)
        invoice_lines = invoice.line_ids.filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled
        )
        
        # Reconcile nếu có lines
        if payment_lines and invoice_lines:
            try:
                (payment_lines + invoice_lines).reconcile()
            except Exception as e:
                # Log lỗi nhưng không raise để không làm gián đoạn quá trình
                import logging
                _logger = logging.getLogger(__name__)
                _logger.warning(f"Error reconciling payment {self.id} with invoice {invoice.id}: {e}")

