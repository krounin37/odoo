# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    voucher_person_name = fields.Char(
        string='Họ tên người nộp / nhận tiền',
        compute='_compute_voucher_defaults',
        store=True,
        readonly=False,
        help='Tên người trực tiếp nộp tiền hoặc nhận tiền mặt/chuyển khoản'
    )

    voucher_address = fields.Char(
        string='Địa chỉ',
        compute='_compute_voucher_defaults',
        store=True,
        readonly=False,
        help='Địa chỉ hoặc bộ phận của người nộp / nhận tiền'
    )

    voucher_reason = fields.Char(
        string='Lý do nộp / chi tiền',
        compute='_compute_voucher_reason',
        store=True,
        readonly=False,
        help='Diễn giải lý do thu/chi tiền in trên chứng từ'
    )

    voucher_attached = fields.Char(
        string='Kèm theo chứng từ gốc',
        default='01',
        help='Số lượng hoặc tên các chứng từ gốc kèm theo (ví dụ: 01 Hóa đơn GTGT, Giấy đề nghị tạm ứng,...)'
    )

    voucher_debit_account = fields.Char(
        string='Tài khoản Nợ',
        compute='_compute_voucher_accounts'
    )

    voucher_credit_account = fields.Char(
        string='Tài khoản Có',
        compute='_compute_voucher_accounts'
    )

    @api.depends('partner_id')
    def _compute_voucher_defaults(self):
        for pay in self:
            if not pay.voucher_person_name and pay.partner_id:
                pay.voucher_person_name = pay.partner_id.name or ''
            if not pay.voucher_address and pay.partner_id:
                address_parts = [p for p in [pay.partner_id.street, pay.partner_id.city] if p]
                pay.voucher_address = ', '.join(address_parts) if address_parts else ''

    @api.depends('memo', 'ref', 'name')
    def _compute_voucher_reason(self):
        for pay in self:
            if not pay.voucher_reason:
                pay.voucher_reason = pay.memo or pay.ref or f"Thanh toán {pay.name}"

    @api.depends('move_id', 'move_id.line_ids')
    def _compute_voucher_accounts(self):
        for pay in self:
            if pay.move_id and pay.move_id.line_ids:
                debit_lines = pay.move_id.line_ids.filtered(lambda l: l.debit > 0)
                credit_lines = pay.move_id.line_ids.filtered(lambda l: l.credit > 0)
                pay.voucher_debit_account = ', '.join(set(debit_lines.mapped('account_id.code'))) or ''
                pay.voucher_credit_account = ', '.join(set(credit_lines.mapped('account_id.code'))) or ''
            else:
                pay.voucher_debit_account = ''
                pay.voucher_credit_account = ''
