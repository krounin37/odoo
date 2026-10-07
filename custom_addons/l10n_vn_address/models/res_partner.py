# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    district_id = fields.Many2one(
        'res.district',
        string='Quận / Huyện',
        domain="[('state_id', '=?', state_id)]",
        help='Chọn Quận / Huyện / Thị xã'
    )
    ward_id = fields.Many2one(
        'res.ward',
        string='Phường / Xã',
        domain="[('district_id', '=?', district_id)]",
        help='Chọn Phường / Xã / Thị trấn'
    )

    @api.onchange('state_id')
    def _onchange_state_id_vn(self):
        if self.state_id and self.district_id and self.district_id.state_id != self.state_id:
            self.district_id = False
            self.ward_id = False

    @api.onchange('district_id')
    def _onchange_district_id_vn(self):
        if self.district_id:
            self.state_id = self.district_id.state_id
            if self.district_id.country_id:
                self.country_id = self.district_id.country_id
            if self.ward_id and self.ward_id.district_id != self.district_id:
                self.ward_id = False

    @api.onchange('ward_id')
    def _onchange_ward_id_vn(self):
        if self.ward_id:
            self.district_id = self.ward_id.district_id
            self.state_id = self.ward_id.state_id
            if self.ward_id.country_id:
                self.country_id = self.ward_id.country_id

    def action_standardize_vn_address(self):
        """Tự động chuẩn hóa chuỗi địa chỉ đầy đủ bao gồm Phường/Xã, Quận/Huyện, Tỉnh/Thành"""
        for partner in self:
            parts = []
            if partner.street:
                parts.append(partner.street.strip().rstrip(','))
            if partner.ward_id:
                parts.append(partner.ward_id.name)
            if partner.district_id:
                parts.append(partner.district_id.name)
            if partner.state_id:
                parts.append(partner.state_id.name)

            if parts:
                partner.street = ', '.join(parts)
        return True
