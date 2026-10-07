# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    misa_endpoint_url = fields.Char(
        string='MISA meInvoice API URL',
        default='https://meinvoiceapi.misa.vn',
        help='Địa chỉ máy chủ API của MISA meInvoice (ví dụ: https://meinvoiceapi.misa.vn)'
    )
    misa_app_id = fields.Char(
        string='MISA App ID',
        help='Mã ứng dụng kết nối do MISA cấp'
    )
    misa_tax_code = fields.Char(
        string='Mã số thuế công ty (MISA)',
        help='Mã số thuế đơn vị bán trên hệ thống MISA'
    )
    misa_username = fields.Char(
        string='Tài khoản MISA'
    )
    misa_password = fields.Char(
        string='Mật khẩu MISA'
    )
    misa_template_code = fields.Char(
        string='Mẫu số hóa đơn',
        default='1C24TYY',
        help='Ký hiệu mẫu hóa đơn đăng ký với cơ quan thuế'
    )
    misa_series = fields.Char(
        string='Ký hiệu hóa đơn (Series)',
        default='C24TYY',
        help='Ký hiệu hóa đơn (ví dụ: C24TYY, K24TYY)'
    )
