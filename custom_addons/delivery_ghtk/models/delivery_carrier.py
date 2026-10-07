# -*- coding: utf-8 -*-
import logging
import requests
from odoo import fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

GHTK_URL_STAGING = 'https://services-staging.ghtklab.com'
GHTK_URL_PROD = 'https://services.giaohangtietkiem.vn'


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(
        selection_add=[('ghtk', 'Giao Hàng Tiết Kiệm (GHTK)')],
        ondelete={'ghtk': 'set default'}
    )
    ghtk_api_token = fields.Char(
        string='GHTK API Token',
        help='Mã xác thực API Partner Token do GHTK cấp trong trang quản trị'
    )
    ghtk_environment = fields.Selection(
        [
            ('staging', 'Thử nghiệm (Staging / GHTK Lab)'),
            ('production', 'Chính thức (Production)'),
        ],
        string='Môi trường GHTK',
        default='staging',
        required=True
    )
    ghtk_pick_address = fields.Char(
        string='Địa chỉ lấy hàng',
        default='Số 10, Đường Cầu Giấy',
        help='Địa chỉ nơi shipper GHTK qua lấy hàng'
    )
    ghtk_pick_province = fields.Char(
        string='Tỉnh/Thành kho lấy',
        default='Hà Nội'
    )
    ghtk_pick_district = fields.Char(
        string='Quận/Huyện kho lấy',
        default='Quận Cầu Giấy'
    )
    ghtk_pick_tel = fields.Char(
        string='Số điện thoại kho lấy',
        default='0901234567'
    )
    ghtk_is_freeship = fields.Selection(
        [
            ('1', 'Shop trả cước vận chuyển (Freeship)'),
            ('0', 'Người nhận trả cước vận chuyển'),
        ],
        string='Cước phí vận chuyển',
        default='1',
        required=True
    )

    def _ghtk_get_base_url(self):
        self.ensure_one()
        return GHTK_URL_PROD if self.ghtk_environment == 'production' else GHTK_URL_STAGING

    def ghtk_rate_shipment(self, order):
        """Tính phí vận chuyển dự tính theo cân nặng và địa chỉ nhận"""
        self.ensure_one()
        partner = order.partner_shipping_id

        # Xác định tỉnh / huyện người nhận
        province = partner.state_id.name if partner.state_id else ''
        district = getattr(partner, 'district_id', False) and partner.district_id.name or partner.city or ''
        address = partner.street or ''

        # Tính tổng trọng lượng đơn hàng (chuyển sang gram)
        total_weight_kg = sum(line.product_id.weight * line.product_uom_qty for line in order.order_line if line.product_id)
        weight_gram = int(max(500, total_weight_kg * 1000))

        # Nếu chưa có Token hoặc chạy thử nghiệm: Tự tính cước giả lập nội tỉnh / liên tỉnh
        if not self.ghtk_api_token:
            if province and self.ghtk_pick_province and province.lower() == self.ghtk_pick_province.lower():
                estimated_fee = 22000.0  # Nội thành
            else:
                estimated_fee = 35000.0  # Liên tỉnh
            return {
                'success': True,
                'price': estimated_fee,
                'error_message': False,
                'warning_message': False,
            }

        url = f"{self._ghtk_get_base_url()}/services/shipment/fee"
        params = {
            'pick_province': self.ghtk_pick_province or 'Hà Nội',
            'pick_district': self.ghtk_pick_district or 'Quận Cầu Giấy',
            'province': province or 'Hà Nội',
            'district': district or 'Quận Cầu Giấy',
            'address': address,
            'weight': weight_gram,
            'value': int(order.amount_total),
        }
        headers = {'Token': self.ghtk_api_token}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            if data.get('success'):
                fee = float(data.get('fee', {}).get('fee', 25000))
                return {
                    'success': True,
                    'price': fee,
                    'error_message': False,
                    'warning_message': False,
                }
            else:
                return {
                    'success': False,
                    'price': 0.0,
                    'error_message': data.get('message', 'Không thể tính phí vận chuyển từ GHTK'),
                    'warning_message': False,
                }
        except Exception as e:
            return {
                'success': False,
                'price': 0.0,
                'error_message': str(e),
                'warning_message': False,
            }

    def ghtk_send_shipping(self, pickings):
        """Đẩy đơn hàng từ Phiếu xuất kho sang hệ thống GHTK"""
        res = []
        for picking in pickings:
            partner = picking.partner_id
            order_name = picking.origin or picking.name

            # Tính trọng lượng
            total_weight_kg = sum(m.product_id.weight * m.quantity for m in picking.move_ids_without_package if m.product_id)
            weight_gram = int(max(500, total_weight_kg * 1000))

            # Nếu chưa cấu hình token thật: Tạo mã vận đơn giả lập để test luồng
            if not self.ghtk_api_token:
                mock_label = f"S{picking.id:04d}.MB01.{picking.id:06d}"
                res.append({
                    'exact_price': 25000.0,
                    'tracking_number': mock_label,
                })
                picking.carrier_tracking_ref = mock_label
                continue

            products_data = []
            for move in picking.move_ids_without_package:
                products_data.append({
                    'name': move.product_id.name or 'Hàng hóa',
                    'weight': max(0.1, move.product_id.weight),
                    'quantity': int(move.quantity or 1),
                })

            order_payload = {
                'products': products_data,
                'order': {
                    'id': f"{picking.name}-{picking.id}",
                    'pick_name': picking.company_id.name,
                    'pick_address': self.ghtk_pick_address,
                    'pick_province': self.ghtk_pick_province,
                    'pick_district': self.ghtk_pick_district,
                    'pick_tel': self.ghtk_pick_tel,
                    'tel': partner.phone or partner.mobile or '0900000000',
                    'name': partner.name,
                    'address': partner.street or '',
                    'province': partner.state_id.name if partner.state_id else '',
                    'district': getattr(partner, 'district_id', False) and partner.district_id.name or partner.city or '',
                    'is_freeship': int(self.ghtk_is_freeship or 1),
                    'pick_money': int(getattr(picking, 'ghtk_cod_amount', 0) or 0),
                    'value': int(getattr(picking, 'voucher_total_amount', 0) or 0),
                    'total_weight': weight_gram / 1000.0,
                }
            }

            url = f"{self._ghtk_get_base_url()}/services/shipment/order"
            headers = {
                'Token': self.ghtk_api_token,
                'Content-Type': 'application/json',
            }

            try:
                resp = requests.post(url, json=order_payload, headers=headers, timeout=15)
                data = resp.json()
                if data.get('success'):
                    label = data.get('order', {}).get('label')
                    fee = float(data.get('order', {}).get('fee', 25000))
                    res.append({
                        'exact_price': fee,
                        'tracking_number': label,
                    })
                    picking.carrier_tracking_ref = label
                else:
                    raise UserError(_("Lỗi từ GHTK: %s") % data.get('message'))
            except Exception as e:
                raise UserError(_("Không thể kết nối đến GHTK: %s") % str(e))

        return res

    def ghtk_get_tracking_link(self, picking):
        """Trả về đường link tra cứu hành trình đơn hàng trên GHTK"""
        if not picking.carrier_tracking_ref:
            return False
        return f"https://khachhang.giaohangtietkiem.vn/khach-hang/don-hang/tra-cuu?label={picking.carrier_tracking_ref}"

    def ghtk_cancel_shipment(self, picking):
        """Hủy đơn hàng trên hệ thống GHTK"""
        if not picking.carrier_tracking_ref or not self.ghtk_api_token:
            return True
        url = f"{self._ghtk_get_base_url()}/services/shipment/cancel/{picking.carrier_tracking_ref}"
        headers = {'Token': self.ghtk_api_token}
        try:
            requests.post(url, headers=headers, timeout=10)
        except Exception as e:
            _logger.warning("Không thể hủy đơn trên GHTK: %s", str(e))
        return True
