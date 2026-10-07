# -*- coding: utf-8 -*-
from odoo import models, fields, api
from .tools import amount_to_vietnamese_words


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_total_words_vn = fields.Char(
        string='Số tiền bằng chữ (VN)',
        compute='_compute_amount_total_words_vn',
        store=True,
        help='Tổng tiền đơn hàng thể hiện bằng chữ Tiếng Việt'
    )

    @api.depends('amount_total', 'currency_id')
    def _compute_amount_total_words_vn(self):
        for order in self:
            currency_name = order.currency_id.name if order.currency_id else 'VND'
            order.amount_total_words_vn = amount_to_vietnamese_words(order.amount_total, currency_name=currency_name)
