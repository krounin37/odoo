# -*- coding: utf-8 -*-
import base64
import re
import urllib.parse
import requests
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    company_partner_id = fields.Many2one(
        'res.partner',
        string='Đối tác công ty',
        related='company_id.partner_id',
        readonly=True
    )

    company_partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Tài khoản nhận tiền (VietQR)',
        compute='_compute_company_partner_bank_id',
        store=True,
        readonly=False,
        domain="[('partner_id', '=', company_partner_id)]",
        help='Chọn tài khoản ngân hàng của công ty dùng để nhận thanh toán cho đơn hàng này'
    )

    vietqr_memo = fields.Char(
        string='Nội dung chuyển khoản VietQR',
        compute='_compute_vietqr_memo',
        store=True,
        readonly=False,
        help='Cú pháp nội dung khách hàng quét mã để chuyển khoản (mặc định là mã đơn hàng)'
    )

    vietqr_url = fields.Char(
        string='Đường dẫn VietQR',
        compute='_compute_vietqr_data',
        store=True,
        help='Link tải ảnh VietQR động'
    )

    vietqr_qr_image = fields.Binary(
        string='Mã VietQR',
        compute='_compute_vietqr_data',
        store=True,
        help='Hình ảnh mã QR chuyển khoản tự động kèm số tiền và nội dung đơn hàng'
    )

    @api.depends('company_id', 'company_id.partner_id.bank_ids')
    def _compute_company_partner_bank_id(self):
        for order in self:
            if not order.company_partner_bank_id:
                banks = order.company_id.partner_id.bank_ids
                order.company_partner_bank_id = banks[:1] if banks else False

    @api.depends('name')
    def _compute_vietqr_memo(self):
        for order in self:
            if not order.vietqr_memo and order.name:
                order.vietqr_memo = f"{order.name} thanh toan"

    @api.depends('company_partner_bank_id', 'amount_total', 'currency_id', 'vietqr_memo')
    def _compute_vietqr_data(self):
        for order in self:
            bank = order.company_partner_bank_id
            clean_acc_val = getattr(bank, 'account_number', None) or getattr(bank, 'acc_number', None) or ''
            if not clean_acc_val:
                order.vietqr_url = False
                order.vietqr_qr_image = False
                continue

            bank_code = bank.get_vietqr_bank_code()
            if not bank_code:
                order.vietqr_url = False
                order.vietqr_qr_image = False
                continue

            clean_acc = re.sub(r'[^0-9a-zA-Z]', '', str(clean_acc_val).strip())
            amount = int(round(order.amount_total or 0))
            memo = order.vietqr_memo or order.name or ''
            holder_name_val = getattr(bank, 'holder_name', None) or getattr(bank, 'acc_holder_name', None) or order.company_id.name or ''
            holder_name = holder_name_val.upper()

            params = {
                'amount': str(amount),
                'addInfo': memo,
                'accountName': holder_name,
            }
            query = urllib.parse.urlencode(params)
            url = f"https://img.vietqr.io/image/{bank_code}-{clean_acc}-compact.png?{query}"
            order.vietqr_url = url

            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    order.vietqr_qr_image = base64.b64encode(resp.content)
                else:
                    order.vietqr_qr_image = False
            except Exception:
                order.vietqr_qr_image = False

    def action_refresh_vietqr(self):
        """Làm mới mã VietQR theo số tiền hoặc nội dung hiện tại"""
        self._compute_vietqr_data()
        return True
