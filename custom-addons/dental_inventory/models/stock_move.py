# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    supply_usage_id = fields.Many2one(
        'supply.usage',
        string='Supply Usage',
        help='Link với supply usage record'
    )

    treatment_session_id = fields.Many2one(
        'treatment.session',
        string='Treatment Session',
        related='supply_usage_id.session_id',
        store=True,
        help='Buổi điều trị sử dụng vật tư'
    )



