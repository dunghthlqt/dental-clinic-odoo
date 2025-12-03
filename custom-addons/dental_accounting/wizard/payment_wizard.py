# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class DentalPaymentWizard(models.TransientModel):
    _name = 'dental.payment.wizard'
    _description = 'Wizard Thanh toán cho Điều trị'
    
    treatment_id = fields.Many2one(
        'dental.treatment',
        string='Điều trị',
        required=True,
        readonly=True
    )
    
    amount = fields.Float(
        'Số tiền thanh toán',
        required=True,
        help='Số tiền khách hàng thanh toán'
    )
    
    min_amount = fields.Float(
        'Số tiền tối thiểu',
        readonly=True,
        help='Số tiền tối thiểu phải thanh toán (phần đóng trước nếu chưa đóng)'
    )
    
    max_amount = fields.Float(
        'Số tiền tối đa',
        readonly=True,
        help='Số tiền còn lại tối đa có thể thanh toán'
    )
    
    payment_date = fields.Date(
        'Ngày thanh toán',
        required=True,
        default=fields.Date.today
    )
    
    @api.model
    def default_get(self, fields_list):
        """Set default values dựa trên treatment và payment plan"""
        res = super().default_get(fields_list)
        
        # Lấy treatment_id từ context hoặc từ res
        treatment_id = res.get('treatment_id') or self.env.context.get('default_treatment_id')
        
        if treatment_id:
            treatment = self.env['dental.treatment'].browse(treatment_id)
            
            # Tính toán remaining_amount
            treatment._compute_remaining_amount()
            remaining_amount = treatment.remaining_amount
            
            # Tính max_amount = remaining_amount
            if 'max_amount' in fields_list:
                res['max_amount'] = remaining_amount
            
            # Nếu là trả góp và có payment plan
            if treatment.payment_policy == 'installment' and treatment.payment_plan_id:
                payment_plan = treatment.payment_plan_id
                upfront_payment = payment_plan.upfront_payment
                total_paid = payment_plan.total_paid
                
                # Nếu chưa thanh toán phần đóng trước
                if total_paid < upfront_payment:
                    # Set min_amount = phần đóng trước còn lại
                    min_amount = upfront_payment - total_paid
                    if 'min_amount' in fields_list:
                        res['min_amount'] = min_amount
                    if 'amount' in fields_list:
                        res['amount'] = min_amount  # Tự động điền phần đóng trước
                else:
                    # Đã thanh toán >= phần đóng trước, thanh toán linh hoạt
                    if 'min_amount' in fields_list:
                        res['min_amount'] = 0.0
                    if 'amount' in fields_list:
                        res['amount'] = remaining_amount  # Default = remaining_amount
            else:
                # Không phải trả góp, thanh toán linh hoạt
                if 'min_amount' in fields_list:
                    res['min_amount'] = 0.0
                if 'amount' in fields_list:
                    res['amount'] = remaining_amount
        
        return res
    
    @api.constrains('amount')
    def _check_amount(self):
        """Kiểm tra số tiền thanh toán không vượt quá số tiền còn lại và không nhỏ hơn min_amount"""
        for wizard in self:
            if wizard.amount <= 0:
                raise ValidationError('Số tiền thanh toán phải lớn hơn 0')
            
            if wizard.amount < wizard.min_amount:
                raise ValidationError(
                    f'Số tiền thanh toán ({wizard.amount:,.0f}) '
                    f'không được nhỏ hơn số tiền tối thiểu ({wizard.min_amount:,.0f})'
                )
            
            if wizard.amount > wizard.max_amount:
                raise ValidationError(
                    f'Số tiền thanh toán ({wizard.amount:,.0f}) '
                    f'không được vượt quá số tiền còn lại ({wizard.max_amount:,.0f})'
                )
    
    def action_confirm_payment(self):
        """Xác nhận thanh toán: Tạo payment, invoice và mở PDF"""
        self.ensure_one()
        
        treatment = self.treatment_id
        
        # Tìm hoặc tạo partner từ patient
        partner = self.env['res.partner'].search([
            ('phone', '=', treatment.patient_id.phone)
        ], limit=1)
        
        if not partner:
            partner = self.env['res.partner'].create({
                'name': treatment.patient_id.name,
                'phone': treatment.patient_id.phone,
                'email': treatment.patient_id.email,
            })
        
        # Tìm journal mặc định cho customer payment
        journal = self.env['account.journal'].search([
            ('type', '=', 'bank'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        
        if not journal:
            journal = self.env['account.journal'].search([
                ('type', 'in', ['bank', 'cash']),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        if not journal:
            raise UserError('Không tìm thấy sổ nhật ký thanh toán. Vui lòng cấu hình trong Kế toán.')
        
        # Tạo payment
        payment_vals = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': partner.id,
            'amount': self.amount,
            'date': self.payment_date,
            'journal_id': journal.id,
            'dental_treatment_id': treatment.id,
            'auto_create_invoice': True,
        }
        
        # Link với payment plan nếu có
        if treatment.payment_plan_id:
            payment_vals['payment_plan_id'] = treatment.payment_plan_id.id
        
        payment = self.env['account.payment'].create(payment_vals)
        
        # Post payment (sẽ tự động tạo invoice)
        payment.action_post()
        
        # Tìm invoice vừa được tạo
        invoice = self.env['account.move'].search([
            ('dental_treatment_id', '=', treatment.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ], order='create_date desc', limit=1)
        
        if not invoice:
            raise UserError('Không tìm thấy hóa đơn vừa được tạo')
        
        # Cập nhật paid_amount trong treatment
        treatment._compute_revenue()
        treatment._compute_remaining_amount()
        
        # Hiển thị thông báo thành công và mở form view của invoice
        # User có thể click nút "Print" trên form view để in PDF
        # (Tránh lỗi PyPDF2 khi mở PDF trực tiếp)
        return {
            'type': 'ir.actions.act_window',
            'name': f'Hóa đơn đã tạo - {invoice.name}',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'create': False,
                'edit': False,
            },
        }

