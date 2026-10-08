# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    vn_province_code = fields.Char(
        string='Mã tỉnh (2 số)',
        help='Mã đơn vị hành chính cấp tỉnh 2 số theo Quyết định chuẩn quốc gia (ví dụ: 01, 79, 31, 48...)'
    )
    vn_code_short = fields.Char(
        string='Mã viết tắt (3 ký tự)',
        help='Mã viết tắt chuẩn 3 ký tự (ví dụ: HNI, HCM, HPG, DNG, TTH, CTO...)'
    )
    vn_place_type = fields.Selection(
        [
            ('city', 'Thành phố Trung Ương'),
            ('province', 'Tỉnh'),
        ],
        string='Loại đơn vị hành chính',
        default='province'
    )
    vn_is_merged = fields.Boolean(
        string='Hình thành sau sắp xếp',
        default=False,
        help='Đánh dấu tỉnh/thành phố được hợp nhất/sáp nhập theo Nghị quyết số 202/2025/QH15'
    )
    vn_merged_with = fields.Char(
        string='Sáp nhập cùng',
        help='Danh sách các tỉnh thành cũ hợp nhất thành đơn vị hành chính mới này'
    )
    vn_administrative_center = fields.Char(
        string='Trung tâm hành chính',
        help='Địa điểm đặt trung tâm chính trị - hành chính của tỉnh/thành phố'
    )
    vn_ward_ids = fields.One2many(
        'res.ward',
        'state_id',
        string='Danh sách Phường / Xã mới (2 cấp)'
    )
