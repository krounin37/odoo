# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    ghtk_cod_amount = fields.Monetary(
        string='Tiền thu hộ COD (VNĐ)',
        currency_field='company_currency_id',
        help='Số tiền shipper GHTK thu hộ khi giao hàng đến tay khách'
    )
    ghtk_print_label_url = fields.Char(
        string='Link in tem nhãn GHTK',
        compute='_compute_ghtk_print_label_url'
    )

    @api.depends('carrier_tracking_ref', 'carrier_id')
    def _compute_ghtk_print_label_url(self):
        for picking in self:
            if picking.carrier_id and picking.carrier_id.delivery_type == 'ghtk' and picking.carrier_tracking_ref:
                base_url = picking.carrier_id._ghtk_get_base_url()
                picking.ghtk_print_label_url = f"{base_url}/services/label/{picking.carrier_tracking_ref}"
            else:
                picking.ghtk_print_label_url = False

    def action_ghtk_print_label(self):
        """Mở link in tem nhãn vận đơn A6 của GHTK"""
        self.ensure_one()
        if not self.carrier_tracking_ref:
            raise UserError(_("Phiếu giao hàng này chưa có mã vận đơn GHTK."))
        base_url = self.carrier_id._ghtk_get_base_url() if self.carrier_id else 'https://services.giaohangtietkiem.vn'
        url = f"{base_url}/services/label/{self.carrier_tracking_ref}"
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
