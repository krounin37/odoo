# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResWard(models.Model):
    _name = 'res.ward'
    _description = 'Phường / Xã / Thị trấn (ĐVHC Cấp 2 mới)'
    _order = 'name asc'

    name = fields.Char(string='Tên Phường / Xã', required=True, index=True)
    code = fields.Char(string='Mã Phường / Xã (5 số)', index=True)
    state_id = fields.Many2one(
        'res.country.state',
        string='Tỉnh / Thành phố',
        required=True,
        ondelete='cascade',
        index=True,
        help='Tỉnh hoặc Thành phố trực thuộc Trung ương quản lý trực tiếp'
    )
    country_id = fields.Many2one(
        'res.country',
        string='Quốc gia',
        related='state_id.country_id',
        store=True,
        readonly=True
    )
    district_id = fields.Many2one(
        'res.district',
        string='Quận / Huyện (cũ / phân vùng)',
        ondelete='set null',
        index=True
    )
    has_merger = fields.Boolean(
        string='Hình thành do sáp nhập',
        default=False
    )
    old_units = fields.Text(
        string='Các đơn vị cũ trước sáp nhập',
        help='Danh sách các xã, phường, thị trấn cũ được sáp nhập thành đơn vị này (dùng để đối soát chuyển đổi địa chỉ)'
    )
    merger_details = fields.Text(
        string='Chi tiết sáp nhập'
    )
    administrative_center = fields.Char(
        string='Trung tâm hành chính'
    )
