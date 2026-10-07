# -*- coding: utf-8 -*-
from odoo import models
from .tools import amount_to_vietnamese_words


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_vn_text(self, amount):
        """Hàm trợ giúp đọc số tiền thành chữ Tiếng Việt gọi từ QWeb template hoặc code"""
        self.ensure_one()
        return amount_to_vietnamese_words(amount, currency_name=self.name)
