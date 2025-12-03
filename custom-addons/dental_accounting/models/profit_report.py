# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class DentalProfitReport(models.TransientModel):
    """Profit Report Wizard - Transient model for reporting"""
    _name = 'dental.profit.report'
    _description = 'Dental Profit Report'

    month = fields.Date(
        'Tháng',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1),
        help='Chọn tháng để xem báo cáo lợi nhuận'
    )
    
    revenue = fields.Float(
        'Doanh thu',
        compute='_compute_profit_data',
        readonly=True,
        help='Tổng doanh thu trong tháng'
    )
    
    supply_cost = fields.Float(
        'Chi phí vật tư',
        compute='_compute_profit_data',
        readonly=True,
        help='Tổng chi phí vật tư trong tháng'
    )
    
    other_costs = fields.Float(
        'Chi phí khác',
        compute='_compute_profit_data',
        readonly=True,
        help='Chi phí cố định (thuê...) từ recurring payments'
    )
    
    salary_cost = fields.Float(
        'Chi phí lương',
        compute='_compute_profit_data',
        readonly=True,
        help='Tổng chi phí lương trong tháng (từ dental_hr)'
    )
    
    total_cost = fields.Float(
        'Tổng chi phí',
        compute='_compute_total_cost',
        readonly=True,
        help='Tổng chi phí = Chi phí vật tư + Chi phí khác + Chi phí lương'
    )
    
    profit = fields.Float(
        'Lợi nhuận',
        compute='_compute_profit',
        readonly=True,
        help='Lợi nhuận = Doanh thu - Tổng chi phí'
    )
    
    @api.depends('month')
    def _compute_profit_data(self):
        """Tính revenue, supply_cost, other_costs, salary_cost từ data"""
        for report in self:
            if not report.month:
                report.revenue = 0.0
                report.supply_cost = 0.0
                report.other_costs = 0.0
                report.salary_cost = 0.0
                continue
            
            # Tính tháng đầu và cuối của tháng được chọn
            month_start = report.month.replace(day=1)
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)
            
            # Tính Revenue: Tổng payments đã posted trong tháng
            payments = self.env['account.payment'].search([
                ('date', '>=', month_start),
                ('date', '<=', month_end),
                ('state', '=', 'posted'),
                ('dental_treatment_id', '!=', False),
            ])
            report.revenue = sum(payments.mapped('amount'))
            
            # Tính Supply Cost: Tổng supply_cost của treatments có payments trong tháng
            # Lấy unique treatments (tránh tính trùng)
            treatments_with_payments = payments.mapped('dental_treatment_id')
            # Tính supply_cost từ treatments (đã được tính tự động từ inventory)
            # Chỉ tính từ treatments có supply_cost > 0 (đã sử dụng vật tư)
            treatments_with_supplies = treatments_with_payments.filtered(lambda t: t.supply_cost > 0)
            report.supply_cost = sum(treatments_with_supplies.mapped('supply_cost')) if treatments_with_supplies else 0.0
            
            # Tính Other Costs: Tổng recurring payments trong tháng
            recurring_moves = self.env['account.move'].search([
                ('date', '>=', month_start),
                ('date', '<=', month_end),
                ('recurring_ref', '!=', False),
                ('state', '=', 'posted'),
            ])
            # Tính tổng debit (chi phí) từ recurring moves
            report.other_costs = sum(recurring_moves.line_ids.filtered(
                lambda l: l.debit > 0
            ).mapped('debit'))
            
            # Tính Salary Cost: Tổng chi phí lương từ dental_hr (chỉ tính lương đã đăng)
            if 'dental.salary' in self.env:
                # Tìm tất cả lương có month trong cùng tháng/năm (không phụ thuộc vào ngày cụ thể)
                # Sử dụng domain để so sánh năm và tháng
                salaries = self.env['dental.salary'].search([
                    ('state', '=', 'posted'),  # Chỉ tính lương đã đăng
                ])
                # Lọc theo tháng/năm vì month có thể là bất kỳ ngày nào trong tháng
                # month trong dental.salary là Date field, cần so sánh năm và tháng
                salaries_in_month = salaries.filtered(
                    lambda s: s.month and 
                    s.month.year == month_start.year and 
                    s.month.month == month_start.month
                )
                report.salary_cost = sum(salaries_in_month.mapped('total_salary')) if salaries_in_month else 0.0
                _logger.info(f"Profit Report - Month: {report.month}, Salary Cost: {report.salary_cost}, Found {len(salaries_in_month)} salaries")
            else:
                report.salary_cost = 0.0
                _logger.warning("Profit Report - dental.salary model not found in environment")
    
    @api.depends('supply_cost', 'other_costs', 'salary_cost')
    def _compute_total_cost(self):
        """Tính tổng chi phí"""
        for report in self:
            report.total_cost = report.supply_cost + report.other_costs + report.salary_cost
    
    @api.depends('revenue', 'total_cost')
    def _compute_profit(self):
        """Tính lợi nhuận"""
        for report in self:
            report.profit = report.revenue - report.total_cost
    
    def action_print_report(self):
        """In báo cáo PDF"""
        self.ensure_one()
        # Tìm report action
        report = self.env['ir.actions.report'].search([
            ('model', '=', 'dental.profit.report'),
            ('report_type', '=', 'qweb-pdf'),
        ], limit=1)
        
        if report:
            # Sử dụng report_action() để mở PDF preview
            action = report.report_action(self, config=False)
            if isinstance(action, dict):
                action['target'] = 'new'
            return action
        else:
            # Fallback: sử dụng URL trực tiếp
            return {
                'type': 'ir.actions.act_url',
                'url': f'/report/pdf/dental_accounting.profit_report_template/{self.id}',
                'target': 'new',
            }

