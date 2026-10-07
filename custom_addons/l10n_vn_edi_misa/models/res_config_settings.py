# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    misa_endpoint_url = fields.Char(
        string='MISA meInvoice API URL',
        related='company_id.misa_endpoint_url',
        readonly=False
    )
    misa_app_id = fields.Char(
        string='MISA App ID',
        related='company_id.misa_app_id',
        readonly=False
    )
    misa_tax_code = fields.Char(
        string='Mã số thuế bên bán (MISA)',
        related='company_id.misa_tax_code',
        readonly=False
    )
    misa_username = fields.Char(
        string='Tài khoản MISA',
        related='company_id.misa_username',
        readonly=False
    )
    misa_password = fields.Char(
        string='Mật khẩu MISA',
        related='company_id.misa_password',
        readonly=False
    )
    misa_template_code = fields.Char(
        string='Mẫu số hóa đơn',
        related='company_id.misa_template_code',
        readonly=False
    )
    misa_series = fields.Char(
        string='Ký hiệu hóa đơn (Series)',
        related='company_id.misa_series',
        readonly=False
    )
