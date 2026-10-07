# -*- coding: utf-8 -*-
from datetime import datetime
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from urllib.parse import urljoin
from odoo.http import request
from .. import const

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Trả về dữ liệu render và URL thanh toán chuyển hướng sang cổng VNPAY"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'vnpay':
            return res

        provider = self.provider_id
        amount_vnpay = int(round(self.amount * 100))
        now_str = datetime.now().strftime('%Y%m%d%H%M%S')
        ip_addr = request.httprequest.remote_addr if request else '127.0.0.1'
        base_url = self.get_base_url()

        params = {
            'vnp_Version': provider.vnpay_version or '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': provider.vnpay_tmn_code or 'DEMOVNPAY',
            'vnp_Amount': str(amount_vnpay),
            'vnp_CreateDate': now_str,
            'vnp_CurrCode': 'VND',
            'vnp_IpAddr': ip_addr,
            'vnp_Locale': 'vn',
            'vnp_OrderInfo': f"Thanh toan don hang {self.reference}",
            'vnp_OrderType': 'other',
            'vnp_ReturnUrl': urljoin(base_url, '/payment/vnpay/return'),
            'vnp_TxnRef': self.reference,
        }

        secure_hash = provider._vnpay_generate_signature(params)
        params['vnp_SecureHash'] = secure_hash

        return {
            'api_url': provider._vnpay_get_api_url(),
            'url_params': params,
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Tìm giao dịch thanh toán trong Odoo theo mã tham chiếu trả về từ VNPAY"""
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'vnpay' or len(tx) == 1:
            return tx

        reference = notification_data.get('vnp_TxnRef')
        if not reference:
            raise ValidationError("VNPAY: Không tìm thấy tham số vnp_TxnRef trong dữ liệu phản hồi.")

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'vnpay')])
        if not tx:
            raise ValidationError(f"VNPAY: Không tìm thấy giao dịch nào khớp với mã tham chiếu {reference}.")
        return tx

    def _process_notification_data(self, notification_data):
        """Xác thực chữ ký và xử lý kết quả giao dịch thanh toán từ VNPAY"""
        super()._process_notification_data(notification_data)
        if self.provider_code != 'vnpay':
            return

        received_hash = notification_data.get('vnp_SecureHash', '')
        params_to_verify = {
            k: v for k, v in notification_data.items()
            if k not in ('vnp_SecureHash', 'vnp_SecureHashType')
        }

        # Kiểm tra chữ ký an toàn nếu có cấu hình hash secret
        if self.provider_id.vnpay_hash_secret:
            expected_hash = self.provider_id._vnpay_generate_signature(params_to_verify)
            if received_hash.lower() != expected_hash.lower():
                _logger.warning("VNPAY: Sai lệch chữ ký xác thực SecureHash cho giao dịch %s", self.reference)
                self._set_error("Chữ ký bảo mật VNPAY SecureHash không hợp lệ.")
                return

        response_code = notification_data.get('vnp_ResponseCode')
        if response_code == '00':
            _logger.info("VNPAY: Giao dịch %s thanh toán thành công.", self.reference)
            self._set_done()
        elif response_code in ('24', '11'):
            _logger.info("VNPAY: Giao dịch %s bị hủy hoặc hết hạn.", self.reference)
            self._set_canceled()
        else:
            err_desc = const.RESPONSE_CODES.get(response_code, f"Mã lỗi VNPAY: {response_code}")
            _logger.warning("VNPAY: Giao dịch %s thất bại: %s", self.reference, err_desc)
            self._set_error(err_desc)
