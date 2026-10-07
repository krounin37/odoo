# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResWard(models.Model):
    _name = 'res.ward'
    _description = 'Phường / Xã / Thị trấn'
    _order = 'name asc'

    name = fields.Char(string='Tên Phường / Xã', required=True, index=True)
    code = fields.Char(string='Mã Phường / Xã', index=True)
    district_id = fields.Many2one(
        'res.district',
        string='Quận / Huyện',
        required=True,
        ondelete='cascade',
        index=True
    )
    state_id = fields.Many2one(
        'res.country.state',
        string='Tỉnh / Thành phố',
        related='district_id.state_id',
        store=True,
        readonly=True
    )
    country_id = fields.Many2one(
        'res.country',
        string='Quốc gia',
        related='district_id.country_id',
        store=True,
        readonly=True
    )
