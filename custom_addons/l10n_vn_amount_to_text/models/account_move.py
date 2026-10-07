# -*- coding: utf-8 -*-
from odoo import models, fields, api
from .tools import amount_to_vietnamese_words


class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_total_words_vn = fields.Char(
        string='Số tiền bằng chữ (VN)',
        compute='_compute_amount_total_words_vn',
        store=True,
        help='Số tiền bằng chữ theo chuẩn ngữ pháp Tiếng Việt và quy định hóa đơn/chứng từ BTC'
    )

    @api.depends('amount_total', 'currency_id')
    def _compute_amount_total_words_vn(self):
        for move in self:
            currency_name = move.currency_id.name if move.currency_id else 'VND'
            move.amount_total_words_vn = amount_to_vietnamese_words(move.amount_total, currency_name=currency_name)
