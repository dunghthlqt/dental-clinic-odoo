# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DentalTreatment(models.Model):
    _inherit = 'dental.treatment'
    
    # Payment Policy
    payment_policy = fields.Selection([
        ('full_payment', 'Thanh toán toàn bộ'),
        ('installment', 'Trả góp'),
    ], string='Chính sách thanh toán', 
       default=None,
       help='Chính sách thanh toán cho điều trị này (tự động cập nhật khi chọn loại điều trị)')
    
    payment_plan_id = fields.Many2one(
        'dental.payment.plan', 
        string='Payment Plan',
        readonly=True,
        help='Payment Plan cho điều trị trả góp'
    )
    
    # Supply Cost (tự động tính từ inventory)
    supply_cost = fields.Float(
        'Chi phí vật tư',
        compute='_compute_supply_cost',
        store=True,
        help='Chi phí vật tư tự động tính từ supply.usage.total_cost'
    )
    
    # Computed field để hiển thị số lượng sessions có vật tư
    supply_sessions_count = fields.Integer(
        'Số buổi có vật tư',
        compute='_compute_supply_sessions_count',
        help='Số lượng buổi điều trị có sử dụng vật tư'
    )
    
    # Computed fields
    revenue = fields.Float(
        'Doanh thu',
        compute='_compute_revenue',
        store=True,
        help='Tổng số tiền đã thu được từ payments'
    )
    
    profit = fields.Float(
        'Lợi nhuận',
        compute='_compute_profit',
        store=True,
        help='Lợi nhuận = Doanh thu - Chi phí vật tư'
    )
    
    remaining_amount = fields.Float(
        'Số tiền còn lại',
        compute='_compute_remaining_amount',
        store=False,
        help='Số tiền còn lại cần thanh toán = Tổng chi phí - Đã thanh toán'
    )
    
    # Override payment_status và paid_amount từ dental_clinic_management để tự động cập nhật
    payment_status = fields.Selection([
        ('unpaid', 'Chưa thanh toán'),
        ('partial', 'Thanh toán một phần'),
        ('paid', 'Đã thanh toán'),
    ], string='Trạng thái thanh toán', 
       compute='_compute_payment_status_and_paid_amount',
       store=True,
       tracking=True,
       readonly=True,
       help='Trạng thái thanh toán tự động cập nhật dựa trên revenue và total_cost')
    
    paid_amount = fields.Float(
        'Đã thanh toán',
        compute='_compute_payment_status_and_paid_amount',
        store=True,
        tracking=True,
        readonly=True,
        help='Số tiền đã thanh toán tự động cập nhật từ revenue'
    )
    
    @api.depends('payment_plan_id', 'payment_plan_id.total_paid', 'payment_plan_id.payment_ids', 'payment_plan_id.payment_ids.state', 'payment_plan_id.payment_ids.amount')
    def _compute_revenue(self):
        """Tính tổng doanh thu từ các payments đã posted"""
        for treatment in self:
            total_revenue = 0.0
            
            # Tính từ payment plan nếu có
            if treatment.payment_plan_id:
                total_revenue = treatment.payment_plan_id.total_paid
            else:
                # Tính từ payments trực tiếp (cho full_payment)
                # Sử dụng search để tìm payments, nhưng cần invalidate cache khi payment thay đổi
                payments = self.env['account.payment'].search([
                    ('dental_treatment_id', '=', treatment.id),
                    ('state', '=', 'posted')
                ])
                total_revenue = sum(payments.mapped('amount'))
            
            treatment.revenue = total_revenue
    
    @api.depends('revenue', 'total_cost', 'payment_plan_id', 'payment_plan_id.total_paid')
    def _compute_payment_status_and_paid_amount(self):
        """Tự động cập nhật payment_status và paid_amount dựa trên revenue và total_cost"""
        for treatment in self:
            # Cập nhật paid_amount = revenue
            treatment.paid_amount = treatment.revenue
            
            # Cập nhật payment_status
            if treatment.total_cost <= 0:
                # Nếu chưa có total_cost hoặc total_cost = 0
                if treatment.revenue <= 0:
                    treatment.payment_status = 'unpaid'
                else:
                    # Đã có thanh toán nhưng chưa có total_cost -> partial
                    treatment.payment_status = 'partial'
            else:
                # Có total_cost, tính toán trạng thái
                if treatment.revenue <= 0:
                    treatment.payment_status = 'unpaid'
                elif treatment.revenue >= treatment.total_cost:
                    treatment.payment_status = 'paid'
                else:
                    treatment.payment_status = 'partial'
    
    @api.depends('session_ids', 'session_ids.supply_ids', 'session_ids.supply_ids.quantity')
    def _compute_supply_cost(self):
        """Tính tổng chi phí vật tư từ tất cả supply usage trong các sessions
        
        Logic:
        - Nếu dental_inventory được cài, dùng total_cost hoặc quantity * unit_cost
        - Nếu không, supply_cost = 0 (chờ dental_inventory được cài)
        - Tự động cập nhật khi supply usage thay đổi
        """
        for treatment in self:
            total_supply_cost = 0.0
            # Lặp qua tất cả sessions
            for session in treatment.session_ids:
                # Lặp qua tất cả supply usage trong session
                for supply in session.supply_ids:
                    # Kiểm tra xem dental_inventory có được cài không (có field product_id)
                    if hasattr(supply, 'product_id') and supply.product_id:
                        # Nếu có total_cost (từ dental_inventory), ưu tiên dùng nó
                        if hasattr(supply, 'total_cost') and supply.total_cost:
                            total_supply_cost += supply.total_cost
                        elif hasattr(supply, 'unit_cost'):
                            # Fallback: tính từ quantity * unit_cost
                            qty = getattr(supply, 'quantity', 0.0) or 0.0
                            unit_cost = getattr(supply, 'unit_cost', 0.0) or 0.0
                            total_supply_cost += qty * unit_cost
            treatment.supply_cost = total_supply_cost
    
    @api.depends('session_ids', 'session_ids.supply_ids')
    def _compute_supply_sessions_count(self):
        """Tính số lượng sessions có sử dụng vật tư"""
        for treatment in self:
            sessions_with_supplies = treatment.session_ids.filtered(
                lambda s: s.supply_ids.filtered(
                    lambda sup: hasattr(sup, 'product_id') and sup.product_id
                )
            )
            treatment.supply_sessions_count = len(sessions_with_supplies)

    @api.depends('revenue', 'supply_cost')
    def _compute_profit(self):
        """Tính lợi nhuận = Doanh thu - Chi phí vật tư"""
        for treatment in self:
            treatment.profit = treatment.revenue - treatment.supply_cost
    
    def _compute_remaining_amount(self):
        """Tính số tiền còn lại cần thanh toán"""
        for treatment in self:
            treatment.remaining_amount = treatment.total_cost - treatment.revenue
    
    @api.model
    def default_get(self, fields_list):
        """Set default payment_policy dựa trên treatment_type nếu có trong context"""
        res = super().default_get(fields_list)
        
        # Nếu có treatment_type trong context (khi tạo mới từ form)
        if 'default_treatment_type' in self.env.context:
            treatment_type = self.env.context.get('default_treatment_type')
            if treatment_type == 'orthodontics':
                res['payment_policy'] = 'installment'
            elif treatment_type:
                res['payment_policy'] = 'full_payment'
        
        return res
    
    @api.model
    def create(self, vals):
        """Override create để tự động set payment_policy dựa trên treatment_type"""
        # Chỉ set payment_policy nếu có treatment_type
        # Nếu không có treatment_type, payment_policy sẽ là None (không hiển thị)
        if 'treatment_type' in vals and vals.get('treatment_type'):
            if vals['treatment_type'] == 'orthodontics':
                vals['payment_policy'] = 'installment'
            else:
                vals['payment_policy'] = 'full_payment'
        # Nếu không có treatment_type hoặc treatment_type là False/None, không set payment_policy
        # (giữ nguyên None hoặc giá trị hiện tại)
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write để tự động cập nhật payment_policy và tạo payment plan khi treatment_type thay đổi"""
        # Nếu treatment_type được thay đổi, tự động cập nhật payment_policy
        if 'treatment_type' in vals:
            if vals['treatment_type'] == 'orthodontics':
                vals['payment_policy'] = 'installment'
            elif vals.get('treatment_type'):
                # Có treatment_type nhưng không phải orthodontics
                vals['payment_policy'] = 'full_payment'
            else:
                # treatment_type bị xóa (set về False/None), set payment_policy về None
                vals['payment_policy'] = None
        
        # Gọi super().write() trước để cập nhật payment_policy
        result = super().write(vals)
        
        # Sau khi write, kiểm tra xem có cần tự động tạo payment plan không
        for treatment in self:
            # Nếu payment_policy = 'installment' và chưa có payment_plan_id và có total_cost
            if (treatment.payment_policy == 'installment' and 
                not treatment.payment_plan_id and 
                treatment.total_cost > 0):
                # Tự động tạo payment plan (sử dụng sudo() để bypass quyền truy cập)
                # Vì đây là hành động tự động của hệ thống, không phải hành động của user
                payment_plan = self.env['dental.payment.plan'].sudo().create({
                    'treatment_id': treatment.id,
                    'upfront_payment_date': fields.Date.today(),
                })
                treatment.payment_plan_id = payment_plan.id
        
        return result
    
    @api.onchange('treatment_type')
    def _onchange_treatment_type(self):
        """Tự động cập nhật payment_policy dựa trên treatment_type (khi thay đổi trong form)"""
        if self.treatment_type == 'orthodontics':
            # Niềng răng = Trả góp
            self.payment_policy = 'installment'
        elif self.treatment_type:
            # Các loại khác = Thanh toán toàn bộ
            self.payment_policy = 'full_payment'
    
    def action_create_payment_plan(self):
        """Tạo Payment Plan cho treatment có payment_policy = 'installment'"""
        self.ensure_one()
        
        if self.payment_policy != 'installment':
            raise models.UserError('Chỉ có thể tạo Payment Plan cho điều trị trả góp')
        
        if self.payment_plan_id:
            raise models.UserError('Treatment này đã có Payment Plan')
        
        # Tạo payment plan
        payment_plan = self.env['dental.payment.plan'].create({
            'treatment_id': self.id,
            'upfront_payment_date': fields.Date.today(),
        })
        
        self.payment_plan_id = payment_plan.id
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment Plan',
            'res_model': 'dental.payment.plan',
            'res_id': payment_plan.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_payment_wizard(self):
        """Mở wizard để nhập số tiền thanh toán"""
        self.ensure_one()
        
        if self.remaining_amount <= 0:
            raise models.UserError('Điều trị này đã thanh toán đủ')
        
        # Tính min_amount dựa trên payment plan
        min_amount = 0.0
        if self.payment_policy == 'installment' and self.payment_plan_id:
            payment_plan = self.payment_plan_id
            upfront_payment = payment_plan.upfront_payment
            total_paid = payment_plan.total_paid
            
            # Nếu chưa thanh toán phần đóng trước
            if total_paid < upfront_payment:
                min_amount = upfront_payment - total_paid
        
        return {
            'name': 'Thanh toán',
            'type': 'ir.actions.act_window',
            'res_model': 'dental.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_treatment_id': self.id,
                'default_max_amount': self.remaining_amount,
                'default_min_amount': min_amount,
            }
        }
    
    def action_view_supply_sessions(self):
        """Mở danh sách sessions có vật tư"""
        self.ensure_one()
        # Tìm các sessions có vật tư
        sessions_with_supplies = self.session_ids.filtered(
            lambda s: s.supply_ids.filtered(lambda sup: sup.product_id)
        )
        
        return {
            'name': 'Buổi điều trị có vật tư',
            'type': 'ir.actions.act_window',
            'res_model': 'treatment.session',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', sessions_with_supplies.ids)],
            'context': {'default_treatment_id': self.id},
        }

