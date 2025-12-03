# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class LowStockAlert(models.Model):
    """Model để gửi notification khi có vật tư tồn kho thấp"""
    _name = 'dental.low.stock.alert'
    _description = 'Low Stock Alert'
    _order = 'create_date desc'

    product_id = fields.Many2one(
        'product.product',
        string='Vật tư',
        required=True,
        domain=[('is_dental_supply', '=', True)],
        ondelete='cascade'
    )
    
    qty_available = fields.Float(
        'Tồn kho hiện tại',
        required=True
    )
    
    min_stock_level = fields.Float(
        'Mức tồn kho tối thiểu',
        required=True
    )
    
    is_resolved = fields.Boolean(
        'Đã xử lý',
        default=False,
        help='Đánh dấu đã xử lý (đã tạo PO hoặc nhập kho)'
    )
    
    resolved_date = fields.Datetime(
        'Ngày xử lý'
    )
    
    resolved_by = fields.Many2one(
        'res.users',
        string='Người xử lý'
    )

    def action_resolve(self):
        """Đánh dấu alert đã được xử lý"""
        self.write({
            'is_resolved': True,
            'resolved_date': fields.Datetime.now(),
            'resolved_by': self.env.user.id
        })
        return True

    @api.model
    def check_low_stock(self):
        """Cron job: Kiểm tra và tạo alerts cho vật tư tồn kho thấp"""
        # Tìm tất cả dental supplies có min_stock_level > 0
        products = self.env['product.product'].search([
            ('is_dental_supply', '=', True),
            ('min_stock_level', '>', 0),
        ])
        
        # Filter products có tồn kho thấp (qty_available < min_stock_level)
        low_stock_products = products.filtered(
            lambda p: p.qty_available < p.min_stock_level
        )
        
        _logger.info(f'Found {len(low_stock_products)} products with low stock')
        
        # Tạo alerts cho các products chưa có alert chưa resolved
        for product in low_stock_products:
            # Kiểm tra xem đã có alert chưa resolved chưa
            existing_alert = self.search([
                ('product_id', '=', product.id),
                ('is_resolved', '=', False)
            ], limit=1)
            
            if not existing_alert:
                # Tạo alert mới
                self.create({
                    'product_id': product.id,
                    'qty_available': product.qty_available,
                    'min_stock_level': product.min_stock_level,
                })
                _logger.info(f'Created low stock alert for {product.name}')
        
        # Tự động resolve các alerts đã không còn low stock
        unresolved_alerts = self.search([('is_resolved', '=', False)])
        for alert in unresolved_alerts:
            # Refresh product để lấy qty_available mới nhất
            alert.product_id.invalidate_recordset(['qty_available', 'is_low_stock'])
            if alert.product_id.qty_available >= alert.product_id.min_stock_level:
                alert.action_resolve()
                _logger.info(f'Auto-resolved alert for {alert.product_id.name}')

