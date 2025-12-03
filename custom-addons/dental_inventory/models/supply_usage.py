# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class SupplyUsage(models.Model):
    _inherit = 'supply.usage'

    product_id = fields.Many2one(
        'product.product',
        string='Vật tư',
        domain=[('is_dental_supply', '=', True)],
        help='Vật tư từ danh mục kho'
    )

    unit_cost = fields.Float(
        'Đơn giá',
        compute='_compute_unit_cost',
        store=True,
        help='Giá mua vào của vật tư (từ PO hoặc standard_price)'
    )

    total_cost = fields.Float(
        'Tổng chi phí',
        compute='_compute_total_cost',
        store=True,
        help='Tổng chi phí = Số lượng × Đơn giá'
    )

    stock_move_id = fields.Many2one(
        'stock.move',
        string='Stock Move',
        readonly=True,
        help='Stock move được tạo khi sử dụng vật tư'
    )

    @api.depends('product_id')
    def _compute_unit_cost(self):
        """Tính unit_cost từ PO hoặc standard_price"""
        for record in self:
            if record.product_id:
                record.unit_cost = record._get_unit_cost_from_po()
            else:
                record.unit_cost = 0.0

    @api.depends('quantity', 'unit_cost')
    def _compute_total_cost(self):
        """Tính total_cost = quantity * unit_cost"""
        for record in self:
            record.total_cost = record.quantity * record.unit_cost

    def _get_unit_cost_from_po(self):
        """Lấy unit_cost từ purchase order line gần nhất"""
        self.ensure_one()
        if not self.product_id:
            return 0.0

        # Tìm purchase order line gần nhất
        # Note: Cannot use order='order_id.date_order desc' in Odoo 17
        # Search all matching lines and sort in Python
        po_lines = self.env['purchase.order.line'].search([
            ('product_id', '=', self.product_id.id),
            ('order_id.state', 'in', ['purchase', 'done']),
        ])
        
        if po_lines:
            # Sort by order date descending and get the most recent one
            # Use max() to find the line with the latest date_order
            latest_date = max(po_lines.mapped('order_id.date_order'), default=None)
            if latest_date:
                po_line = po_lines.filtered(lambda l: l.order_id.date_order == latest_date)[0]
                return po_line.price_unit

        # Fallback về standard_price
        return self.product_id.standard_price or 0.0

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Tự động fill thông tin khi chọn product"""
        if self.product_id:
            # Auto-fill name từ product
            self.name = self.product_id.name
            
            # Auto-fill supply_code từ product.default_code
            if self.product_id.default_code:
                self.supply_code = self.product_id.default_code
            
            # Auto-fill unit_cost
            self.unit_cost = self._get_unit_cost_from_po()
        else:
            self.name = False
            self.supply_code = False
            self.unit_cost = 0.0

    @api.onchange('quantity')
    def _onchange_quantity(self):
        """Recompute total_cost khi quantity thay đổi"""
        # total_cost sẽ tự động được recompute qua @api.depends
        pass

    @api.model_create_multi
    def create(self, vals_list):
        """Override create để tự động fill name từ product_id nếu chưa có"""
        for vals in vals_list:
            # Nếu có product_id nhưng chưa có name, tự động fill name
            if vals.get('product_id') and not vals.get('name'):
                product = self.env['product.product'].browse(vals['product_id'])
                vals['name'] = product.name
                # Auto-fill supply_code nếu có
                if product.default_code and not vals.get('supply_code'):
                    vals['supply_code'] = product.default_code
        return super().create(vals_list)

    def _create_stock_move(self):
        """Tạo stock move và tự động trừ tồn kho - sử dụng cách tương tự Scrap của Odoo"""
        self.ensure_one()
        
        if self.stock_move_id:
            # Đã có stock move rồi
            return self.stock_move_id

        if not self.product_id:
            raise UserError('Vui lòng chọn vật tư trước khi hoàn thành buổi điều trị.')

        if not self.session_id:
            raise UserError('Supply usage phải liên kết với treatment session.')

        import logging
        _logger = logging.getLogger(__name__)

        # Tìm warehouse và location
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        if not warehouse:
            warehouse = self.env['stock.warehouse'].search([], limit=1)
        if not warehouse:
            raise UserError('Không tìm thấy warehouse. Vui lòng cấu hình warehouse trong Inventory.')

        location_src = warehouse.lot_stock_id  # WH/Stock
        
        # Location đích: Scrap location (Virtual Locations / Scrap)
        # Sử dụng scrap location thay vì inventory loss
        location_dest = self.env['stock.location'].search([
            ('scrap_location', '=', True),
            ('company_id', 'in', [self.env.company.id, False]),
        ], limit=1)
        
        if not location_dest:
            location_dest = self.env.ref('stock.stock_location_scrapped', raise_if_not_found=False)
        
        if not location_dest:
            raise UserError('Không tìm thấy Scrap location. Vui lòng cấu hình stock locations.')

        _logger.info(f'Tạo stock move cho supply usage {self.id}: product={self.product_id.name}, qty={self.quantity}')
        _logger.info(f'Location: {location_src.complete_name} -> {location_dest.complete_name}')

        # Tạo stock move với move_line_ids inline và picked=True
        # Đây là cách Odoo Scrap làm - quan trọng!
        move_vals = {
            'name': f'Tiêu hao: {self.product_id.name} - Session #{self.session_id.id}',
            'origin': f'Treatment Session #{self.session_id.id}',
            'company_id': self.env.company.id,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'product_uom_qty': self.quantity,
            'state': 'draft',
            'location_id': location_src.id,
            'location_dest_id': location_dest.id,
            'scrapped': True,  # Đánh dấu là scrapped/consumed
            'supply_usage_id': self.id,
            # Tạo move_line inline - quan trọng cho Odoo 17!
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'product_uom_id': self.product_id.uom_id.id,
                'quantity': self.quantity,
                'location_id': location_src.id,
                'location_dest_id': location_dest.id,
                'company_id': self.env.company.id,
            })],
            'picked': True,  # Quan trọng trong Odoo 17!
        }
        
        stock_move = self.env['stock.move'].create(move_vals)
        _logger.info(f'Stock move {stock_move.id} created with move_line, state: {stock_move.state}')

        # Validate stock move - sử dụng context is_scrap như Odoo Scrap
        stock_move.with_context(is_scrap=True)._action_done()
        _logger.info(f'Stock move {stock_move.id} after _action_done, state: {stock_move.state}')

        # Kiểm tra state sau khi done
        if stock_move.state == 'done':
            _logger.info(f'✅ Stock move {stock_move.id} validated successfully - tồn kho đã trừ')
        else:
            _logger.error(f'❌ Stock move {stock_move.id} state is {stock_move.state}, expected done')

        # Link stock_move_id
        self.stock_move_id = stock_move.id
        
        return stock_move

    def write(self, vals):
        """Override write để tự động fill name từ product_id và tạo stock move khi session completed"""
        # Tự động fill name từ product_id nếu có product_id nhưng chưa có name
        if vals.get('product_id') and not vals.get('name'):
            product = self.env['product.product'].browse(vals['product_id'])
            vals['name'] = product.name
            # Auto-fill supply_code nếu có
            if product.default_code and not vals.get('supply_code'):
                vals['supply_code'] = product.default_code
        
        result = super().write(vals)
        
        for record in self:
            # Đảm bảo name luôn được fill từ product_id nếu có product_id nhưng chưa có name
            if record.product_id and not record.name:
                record.name = record.product_id.name
                if record.product_id.default_code and not record.supply_code:
                    record.supply_code = record.product_id.default_code
            
            # Kiểm tra nếu session đã completed và chưa có stock_move_id
            if (record.session_id and 
                record.session_id.status == 'completed' and 
                not record.stock_move_id and
                record.product_id):
                try:
                    record._create_stock_move()
                except Exception as e:
                    # Log error nhưng không block write
                    import logging
                    _logger = logging.getLogger(__name__)
                    _logger.warning(f'Không thể tạo stock move cho supply usage {record.id}: {str(e)}')
        
        return result

    def unlink(self):
        """Override unlink để hủy stock move nếu chưa validate"""
        for record in self:
            if record.stock_move_id:
                # Chỉ hủy nếu stock move chưa được validate
                if record.stock_move_id.state in ('draft', 'waiting', 'confirmed'):
                    record.stock_move_id._action_cancel()
                    record.stock_move_id.unlink()
        
        return super().unlink()

