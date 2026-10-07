# -*- coding: utf-8 -*-
import hashlib
import hmac
import urllib.parse
from odoo import fields, models
from .. import const


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('vnpay', 'VNPAY')],
        ondelete={'vnpay': 'set default'}
    )
    vnpay_tmn_code = fields.Char(
        string='Mã Website VNPAY (TMN Code)',
        help='Mã Terminal ID website được cấp bởi VNPAY (ví dụ: DEMOVNPAY)',
        required_if_provider='vnpay',
        copy=False
    )
    vnpay_hash_secret = fields.Char(
        string='Chuỗi bí mật tạo chữ ký (Hash Secret)',
        help='Khóa bí mật tạo chữ ký số HMAC-SHA512 do VNPAY cung cấp',
        required_if_provider='vnpay',
        copy=False,
        groups='base.group_system'
    )
    vnpay_version = fields.Char(
        string='Phiên bản VNPAY',
        default='2.1.0',
        help='Phiên bản API của cổng thanh toán VNPAY'
    )

    def _vnpay_get_api_url(self):
        """Trả về URL cổng thanh toán tương ứng môi trường Test (Sandbox) hoặc Live"""
        self.ensure_one()
        if self.state == 'enabled':
            return const.VNPAY_PROD_URL
        return const.VNPAY_SANDBOX_URL

    def _vnpay_generate_signature(self, params):
        """Tạo mã xác thực an toàn HMAC-SHA512 theo thứ tự alphabet các tham số"""
        self.ensure_one()
        secret = (self.vnpay_hash_secret or '').strip().encode('utf-8')
        sorted_keys = sorted(params.keys())
        query_items = []
        for k in sorted_keys:
            val = str(params[k])
            query_items.append(f"{k}={urllib.parse.quote_plus(val)}")
        raw_hash_data = "&".join(query_items)
        return hmac.new(secret, raw_hash_data.encode('utf-8'), hashlib.sha512).hexdigest()
