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
        domain="[('state_id', '=?', state_id)]",
        help='Chọn Phường / Xã / Thị trấn (Đơn vị hành chính cấp 2 mới)'
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
            # Đồng bộ vào city để tương thích với các phân hệ Odoo chuẩn (eCommerce, Invoicing, Delivery)
            self.city = self.district_id.name
            if self.ward_id and self.ward_id.district_id != self.district_id:
                self.ward_id = False

    @api.onchange('ward_id')
    def _onchange_ward_id_vn(self):
        if self.ward_id:
            if self.ward_id.state_id:
                self.state_id = self.ward_id.state_id
            if self.ward_id.country_id:
                self.country_id = self.ward_id.country_id
            if self.ward_id.district_id:
                self.district_id = self.ward_id.district_id
                self.city = self.district_id.name
            elif self.ward_id.state_id:
                self.city = self.ward_id.state_id.name

    def _prepare_display_address(self, without_company=False):
        """Kế thừa định dạng hiển thị địa chỉ của Odoo để đưa Phường/Xã vào mẫu địa chỉ Việt Nam 2 cấp mới"""
        address_format, args = super()._prepare_display_address(without_company=without_company)
        if self.ward_id:
            args['ward_name'] = self.ward_id.name or ''
        else:
            args['ward_name'] = ''
        if self.district_id and not self.city:
            self.city = self.district_id.name
        return address_format, args

    def action_convert_legacy_to_new_address(self):
        """Chuyển đổi địa chỉ cũ (3 cấp) sang đơn vị hành chính mới (2 cấp) theo Nghị quyết 202/2025/QH15 (dvhcvn/34tinhthanh)"""
        for partner in self:
            full_text = f"{partner.street or ''} {partner.city or ''}"
            if not full_text.strip():
                continue

            Ward = self.env['res.ward']
            matched_ward = None
            matched_old_unit = None

            # 1. Tìm kiếm trong danh mục xã/phường mới (3.321 đơn vị)
            # Ưu tiên tìm trong các đơn vị thuộc tỉnh hiện tại nếu đã chọn state_id
            domain = [('state_id', '=', partner.state_id.id)] if partner.state_id else []
            candidate_wards = Ward.search(domain)

            for w in candidate_wards:
                # Kiểm tra trực tiếp tên xã mới
                if w.name and w.name.lower() in full_text.lower():
                    matched_ward = w
                    break
                # Kiểm tra danh sách đơn vị cũ (old_units) đã được sáp nhập thành xã này
                if w.old_units:
                    for old_u in w.old_units.split(','):
                        clean_old = old_u.strip()
                        if clean_old and clean_old.lower() in full_text.lower():
                            matched_ward = w
                            matched_old_unit = clean_old
                            break
                    if matched_ward:
                        break

            # Nếu chưa tìm thấy và chưa lọc tỉnh, tìm toàn quốc
            if not matched_ward and partner.state_id:
                for w in Ward.search([]):
                    if w.old_units:
                        for old_u in w.old_units.split(','):
                            clean_old = old_u.strip()
                            if clean_old and clean_old.lower() in full_text.lower():
                                matched_ward = w
                                matched_old_unit = clean_old
                                break
                        if matched_ward:
                            break

            if matched_ward:
                partner.ward_id = matched_ward.id
                if matched_ward.state_id:
                    partner.state_id = matched_ward.state_id
                vn = self.env.ref('base.vn', raise_if_not_found=False)
                if vn:
                    partner.country_id = vn.id
                
                msg = f"Đã chuyển đổi thành công sang: {matched_ward.name}, {matched_ward.state_id.name}"
                if matched_old_unit:
                    msg = f"Đã nhận diện đơn vị cũ '{matched_old_unit}' → Chuyển sang: {matched_ward.name}, {matched_ward.state_id.name}"
                    
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Chuyển đổi ĐVHC thành công!'),
                        'message': msg,
                        'type': 'success',
                        'sticky': False,
                    }
                }
        return True

    def action_standardize_vn_address(self):
        """Tự động chuẩn hóa chuỗi địa chỉ đầy đủ bao gồm Phường/Xã, Quận/Huyện, Tỉnh/Thành"""
        for partner in self:
            parts = []
            if partner.street:
                clean_street = partner.street.strip().rstrip(',')
                parts.append(clean_street)
            if partner.ward_id and partner.ward_id.name not in (partner.street or ''):
                parts.append(partner.ward_id.name)
            if partner.district_id and partner.district_id.name not in (partner.street or ''):
                parts.append(partner.district_id.name)
            if partner.state_id and partner.state_id.name not in (partner.street or ''):
                parts.append(partner.state_id.name)

            if parts:
                partner.street = ', '.join(parts)
        return True
