# -*- coding: utf-8 -*-
import json
import logging
from werkzeug.exceptions import Forbidden
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class VNPayController(http.Controller):
    _return_url = '/payment/vnpay/return'
    _ipn_url = '/payment/vnpay/ipn'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False, save_session=False)
    def vnpay_return_from_checkout(self, **data):
        """Xử lý điều hướng khách hàng quay trở lại website sau khi thanh toán trên cổng VNPAY"""
        _logger.info("VNPAY: Nhận dữ liệu chuyển hướng (Return URL): %s", data)
        try:
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data('vnpay', data)
            tx_sudo._handle_notification_data('vnpay', data)
        except ValidationError as e:
            _logger.warning("VNPAY: Lỗi xác thực dữ liệu Return URL: %s", str(e))

        return request.redirect('/payment/status')

    @http.route(_ipn_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def vnpay_ipn_webhook(self, **data):
        """Nhận Webhook ngầm Server-to-Server (IPN) từ hệ thống VNPAY"""
        _logger.info("VNPAY: Nhận thông báo giao dịch IPN từ VNPAY: %s", data)
        try:
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data('vnpay', data)
            tx_sudo._handle_notification_data('vnpay', data)
            response = {'RspCode': '00', 'Message': 'Confirm Success'}
        except ValidationError:
            response = {'RspCode': '01', 'Message': 'Order not found'}
        except Exception as e:
            _logger.error("VNPAY: Lỗi xử lý IPN: %s", str(e))
            response = {'RspCode': '99', 'Message': 'Unknown error'}

        return request.make_response(
            json.dumps(response),
            headers=[('Content-Type', 'application/json')]
        )
