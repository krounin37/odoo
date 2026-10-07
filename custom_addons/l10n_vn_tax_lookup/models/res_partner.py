# -*- coding: utf-8 -*-
import re
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vn_tax_status = fields.Char(
        string='Trạng thái thuế',
        readonly=True,
        copy=False,
        help='Trạng thái hoạt động của Người Nộp Thuế từ cơ quan thuế'
    )
    vn_international_name = fields.Char(
        string='Tên giao dịch quốc tế',
        copy=False,
        help='Tên tiếng Anh / quốc tế của doanh nghiệp'
    )
    vn_short_name = fields.Char(
        string='Tên viết tắt',
        copy=False
    )

    def action_lookup_tax_info(self):
        """Gọi API tra cứu thông tin doanh nghiệp theo Mã Số Thuế"""
        self.ensure_one()
        if not self.vat:
            raise UserError(_("Vui lòng nhập Mã số thuế (Mã số DN) trước khi thực hiện tra cứu."))

        clean_vat = re.sub(r'[^0-9\-]', '', self.vat.strip())
        if not clean_vat:
            raise UserError(_("Mã số thuế không hợp lệ."))

        url = f"https://api.vietqr.io/v2/business/{clean_vat}"
        try:
            response = requests.get(url, timeout=8)
            res_json = response.json()
        except requests.exceptions.Timeout:
            raise UserError(_("Không thể kết nối đến máy chủ tra cứu mã số thuế (Quá thời gian chờ)."))
        except Exception as e:
            raise UserError(_("Đã xảy ra lỗi khi tra cứu mã số thuế: %s") % str(e))

        if res_json.get('code') != '00' or not res_json.get('data'):
            desc = res_json.get('desc', _('Không tìm thấy thông tin người nộp thuế.'))
            raise UserError(_("Tra cứu thất bại: %s") % desc)

        data = res_json['data']
        company_name = data.get('name') or ''
        company_address = data.get('address') or ''
        status = data.get('status') or ''
        international_name = data.get('internationalName') or ''
        short_name = data.get('shortName') or ''

        vals = {
            'is_company': True,
            'vn_tax_status': status,
        }

        if company_name:
            vals['name'] = company_name
        if company_address:
            vals['street'] = company_address
        if international_name:
            vals['vn_international_name'] = international_name
        if short_name:
            vals['vn_short_name'] = short_name

        self.write(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Tra cứu thành công!'),
                'message': _('Đã cập nhật thông tin: %s (Trạng thái: %s)') % (company_name, status or 'Đang hoạt động'),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
