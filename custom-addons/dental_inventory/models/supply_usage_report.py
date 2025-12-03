# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from collections import defaultdict


class SupplyUsageReport(models.TransientModel):
    """Wizard để tạo báo cáo sử dụng vật tư"""
    _name = 'dental.supply.usage.report'
    _description = 'Supply Usage Report'

    date_from = fields.Date(
        'Từ ngày',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1),
        help='Ngày bắt đầu của báo cáo'
    )
    
    date_to = fields.Date(
        'Đến ngày',
        required=True,
        default=lambda self: fields.Date.today(),
        help='Ngày kết thúc của báo cáo'
    )
    
    group_by = fields.Selection([
        ('product', 'Theo sản phẩm'),
        ('category', 'Theo phân loại'),
        ('treatment', 'Theo loại điều trị'),
        ('month', 'Theo tháng'),
    ], string='Nhóm theo', default='product', required=True)
    
    # Report data fields (readonly, computed)
    report_line_ids = fields.One2many(
        'dental.supply.usage.report.line',
        'report_id',
        string='Chi tiết báo cáo',
        readonly=True
    )
    
    total_quantity = fields.Float(
        'Tổng số lượng',
        compute='_compute_totals',
        readonly=True
    )
    
    total_cost = fields.Float(
        'Tổng chi phí',
        compute='_compute_totals',
        readonly=True
    )

    @api.depends('report_line_ids')
    def _compute_totals(self):
        """Tính tổng số lượng và chi phí"""
        for report in self:
            report.total_quantity = sum(report.report_line_ids.mapped('quantity'))
            report.total_cost = sum(report.report_line_ids.mapped('total_cost'))

    def action_generate_report(self):
        """Tạo báo cáo dựa trên filters"""
        self.ensure_one()
        
        # Xóa các dòng cũ
        self.report_line_ids.unlink()
        
        # Tìm tất cả supply usage trong khoảng thời gian
        # Supply usage được tạo khi treatment session completed
        # Cần tìm qua treatment.session
        sessions = self.env['treatment.session'].search([
            ('status', '=', 'completed'),
            ('session_date', '>=', self.date_from),
            ('session_date', '<=', self.date_to),
        ])
        
        # Lấy tất cả supply_ids từ sessions
        supply_usages = self.env['supply.usage']
        for session in sessions:
            supply_usages |= session.supply_ids.filtered(
                lambda s: s.product_id and s.total_cost > 0
            )
        
        if not supply_usages:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'message': 'Không có dữ liệu sử dụng vật tư trong khoảng thời gian đã chọn.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Group data theo group_by
        grouped_data = defaultdict(lambda: {'quantity': 0.0, 'total_cost': 0.0, 'unit_cost': 0.0})
        
        for usage in supply_usages:
            if self.group_by == 'product':
                key = usage.product_id.id
                name = usage.product_id.name or 'N/A'
            elif self.group_by == 'category':
                if usage.product_id.supply_category_id:
                    key = usage.product_id.supply_category_id.id
                    name = usage.product_id.supply_category_id.name
                else:
                    key = 0
                    name = 'Không phân loại'
            elif self.group_by == 'treatment':
                if usage.session_id and usage.session_id.treatment_id:
                    key = usage.session_id.treatment_id.id
                    name = usage.session_id.treatment_id.name or f'Treatment #{usage.session_id.treatment_id.id}'
                else:
                    key = 0
                    name = 'Không xác định'
            else:  # month
                if usage.session_id and usage.session_id.session_date:
                    month = usage.session_id.session_date.strftime('%Y-%m')
                else:
                    month = 'N/A'
                key = month
                name = month
            
            grouped_data[(key, name)]['quantity'] += usage.quantity
            grouped_data[(key, name)]['total_cost'] += usage.total_cost
        
        # Tạo report lines
        lines = []
        for (key, name), data in sorted(grouped_data.items(), key=lambda x: x[1]['total_cost'], reverse=True):
            if data['quantity'] > 0:
                data['unit_cost'] = data['total_cost'] / data['quantity']
            
            lines.append((0, 0, {
                'report_id': self.id,
                'name': name,
                'quantity': data['quantity'],
                'unit_cost': data['unit_cost'],
                'total_cost': data['total_cost'],
            }))
        
        self.write({'report_line_ids': lines})
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_print_report(self):
        """In báo cáo PDF"""
        return self.env.ref('dental_inventory.action_report_supply_usage').report_action(self)


class SupplyUsageReportLine(models.TransientModel):
    """Dòng trong báo cáo sử dụng vật tư"""
    _name = 'dental.supply.usage.report.line'
    _description = 'Supply Usage Report Line'
    _order = 'total_cost desc'

    report_id = fields.Many2one(
        'dental.supply.usage.report',
        string='Báo cáo',
        required=True,
        ondelete='cascade'
    )
    
    name = fields.Char(
        'Tên',
        required=True
    )
    
    quantity = fields.Float(
        'Số lượng',
        required=True
    )
    
    unit_cost = fields.Float(
        'Đơn giá trung bình',
        required=True
    )
    
    total_cost = fields.Float(
        'Tổng chi phí',
        required=True
    )

