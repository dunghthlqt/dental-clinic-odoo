# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class TreatmentSession(models.Model):
    _inherit = 'treatment.session'

    def _create_stock_moves_for_supplies(self):
        """Tạo stock moves cho tất cả supply usages của session này"""
        for record in self:
            if record.status != 'completed':
                continue
                
            _logger.info(f'Đang tạo stock moves cho session {record.id}, có {len(record.supply_ids)} supply usage')
            
            for supply_usage in record.supply_ids:
                _logger.info(f'Kiểm tra supply usage {supply_usage.id}: product_id={supply_usage.product_id.id if supply_usage.product_id else None}, stock_move_id={supply_usage.stock_move_id.id if supply_usage.stock_move_id else None}')
                
                if supply_usage.product_id and not supply_usage.stock_move_id:
                    try:
                        stock_move = supply_usage._create_stock_move()
                        _logger.info(f'✅ Đã tạo stock move {stock_move.id} cho supply usage {supply_usage.id}')
                    except Exception as e:
                        _logger.error(f'❌ Không thể tạo stock move cho supply usage {supply_usage.id}: {str(e)}', exc_info=True)
                elif not supply_usage.product_id:
                    _logger.warning(f'⚠️ Supply usage {supply_usage.id} không có product_id, bỏ qua')

    @api.model_create_multi
    def create(self, vals_list):
        """Override create để tự động tạo stock moves nếu session được tạo với status='completed'"""
        records = super().create(vals_list)
        
        # Tạo stock moves cho các session có status='completed' ngay khi tạo
        completed_sessions = records.filtered(lambda r: r.status == 'completed')
        if completed_sessions:
            _logger.info(f'Tạo mới session với status=completed: {completed_sessions.ids}')
            completed_sessions._create_stock_moves_for_supplies()
        
        return records

    def write(self, vals):
        """Override write để tự động tạo stock moves khi session completed"""
        # Kiểm tra nếu status đang được thay đổi thành 'completed'
        status_changed_to_completed = vals.get('status') == 'completed'
        
        # Lưu lại các session chưa completed trước khi write
        sessions_becoming_completed = self.env['treatment.session']
        if status_changed_to_completed:
            sessions_becoming_completed = self.filtered(lambda r: r.status != 'completed')
            _logger.info(f'Status đang được thay đổi thành completed cho session {sessions_becoming_completed.ids}')
        
        result = super().write(vals)
        
        # Tạo stock moves cho các session vừa chuyển thành completed
        if sessions_becoming_completed:
            sessions_becoming_completed._create_stock_moves_for_supplies()
        
        return result

