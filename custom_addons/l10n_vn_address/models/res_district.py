# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResDistrict(models.Model):
    _name = 'res.district'
    _description = 'Quận / Huyện / Thị xã'
    _order = 'name asc'

    name = fields.Char(string='Tên Quận / Huyện', required=True, index=True)
    code = fields.Char(string='Mã Quận / Huyện', index=True)
    state_id = fields.Many2one(
        'res.country.state',
        string='Tỉnh / Thành phố',
        required=True,
        ondelete='cascade',
        index=True
    )
    country_id = fields.Many2one(
        'res.country',
        string='Quốc gia',
        related='state_id.country_id',
        store=True,
        readonly=True
    )
    ward_ids = fields.One2many(
        'res.ward',
        'district_id',
        string='Danh sách Phường / Xã'
    )
