# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.tools.translate import _


class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_open_change_password_wizard(self):
        """Mở pop-up đặt / đổi mật khẩu trực tiếp cho các người dùng được chọn từ nút bánh răng hoặc form view"""
        return {
            'name': _('Đặt / Đổi Mật Khẩu'),
            'type': 'ir.actions.act_window',
            'res_model': 'change.password.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_model': 'res.users',
                'active_ids': self.ids,
                'active_id': self.ids[0] if self.ids else False,
            }
        }
