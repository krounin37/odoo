# -*- coding: utf-8 -*-
from odoo import models, fields, api
try:
    from odoo.addons.l10n_vn_amount_to_text.models.tools import amount_to_vietnamese_words
except ImportError:
    def amount_to_vietnamese_words(amount, currency_name='VND'):
        return f"{int(amount)} {currency_name}"


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    voucher_contact_person = fields.Char(
        string='Người giao / nhận hàng',
        compute='_compute_voucher_defaults',
        store=True,
        readonly=False,
        help='Họ và tên người giao hàng (nếu nhập kho) hoặc người nhận hàng (nếu xuất kho)'
    )

    voucher_contact_address = fields.Char(
        string='Địa chỉ / Đơn vị',
        compute='_compute_voucher_defaults',
        store=True,
        readonly=False
    )

    voucher_reason = fields.Char(
        string='Lý do nhập / xuất kho',
        compute='_compute_voucher_reason',
        store=True,
        readonly=False
    )

    voucher_attached = fields.Char(
        string='Kèm theo chứng từ gốc',
        default='01'
    )

    voucher_warehouse_name = fields.Char(
        string='Kho nhập / xuất',
        compute='_compute_voucher_warehouse',
        store=True,
        readonly=False
    )

    voucher_warehouse_address = fields.Char(
        string='Địa điểm kho',
        compute='_compute_voucher_warehouse',
        store=True,
        readonly=False
    )

    voucher_debit_account = fields.Char(
        string='Tài khoản Nợ',
        default='156 / 152'
    )

    voucher_credit_account = fields.Char(
        string='Tài khoản Có',
        default='331 / 111 / 632'
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        related='company_id.currency_id',
        readonly=True
    )

    voucher_total_amount = fields.Monetary(
        string='Tổng giá trị vật tư',
        compute='_compute_voucher_totals',
        currency_field='company_currency_id',
        store=True
    )

    voucher_total_words_vn = fields.Char(
        string='Tổng tiền bằng chữ',
        compute='_compute_voucher_totals',
        store=True
    )

    @api.depends('partner_id')
    def _compute_voucher_defaults(self):
        for picking in self:
            if not picking.voucher_contact_person and picking.partner_id:
                picking.voucher_contact_person = picking.partner_id.name or ''
            if not picking.voucher_contact_address and picking.partner_id:
                parts = [p for p in [picking.partner_id.street, picking.partner_id.city] if p]
                picking.voucher_contact_address = ', '.join(parts) if parts else ''

    @api.depends('origin', 'picking_type_id', 'name')
    def _compute_voucher_reason(self):
        for picking in self:
            if not picking.voucher_reason:
                code = picking.picking_type_id.code if picking.picking_type_id else ''
                origin = picking.origin or picking.name or ''
                if code == 'incoming':
                    picking.voucher_reason = f"Nhập kho theo chứng từ {origin}"
                elif code == 'outgoing':
                    picking.voucher_reason = f"Xuất kho bán hàng theo {origin}"
                else:
                    picking.voucher_reason = f"Điều chuyển kho theo {origin}"

    @api.depends('location_id', 'location_dest_id', 'picking_type_id')
    def _compute_voucher_warehouse(self):
        for picking in self:
            code = picking.picking_type_id.code if picking.picking_type_id else ''
            if code == 'incoming':
                loc = picking.location_dest_id
            else:
                loc = picking.location_id
            if loc:
                picking.voucher_warehouse_name = loc.name or ''
                picking.voucher_warehouse_address = loc.complete_name or ''

    @api.depends('move_ids_without_package', 'move_ids_without_package.quantity', 'move_ids_without_package.product_uom_qty')
    def _compute_voucher_totals(self):
        for picking in self:
            total = 0.0
            for move in picking.move_ids_without_package:
                qty = move.quantity if move.quantity else move.product_uom_qty
                price = getattr(move, 'price_unit', 0.0) or (move.product_id.standard_price if move.product_id else 0.0)
                total += qty * price

            picking.voucher_total_amount = total
            currency_name = picking.company_currency_id.name if picking.company_currency_id else 'VND'
            picking.voucher_total_words_vn = amount_to_vietnamese_words(total, currency_name=currency_name)
