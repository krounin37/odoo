# -*- coding: utf-8 -*-
from odoo import models, fields, api
from .tools import amount_to_vietnamese_words


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    amount_words_vn = fields.Char(
        string='Số tiền bằng chữ (VN)',
        compute='_compute_amount_words_vn',
        store=True,
        help='Số tiền bằng chữ phục vụ in phiếu thu, phiếu chi'
    )

    @api.depends('amount', 'currency_id')
    def _compute_amount_words_vn(self):
        for pay in self:
            currency_name = pay.currency_id.name if pay.currency_id else 'VND'
            pay.amount_words_vn = amount_to_vietnamese_words(pay.amount, currency_name=currency_name)
