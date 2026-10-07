# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class VnvatDeclarationWizard(models.TransientModel):
    _name = 'vn.vat.declaration.wizard'
    _description = 'Bảng Kê Hóa Đơn Thuế GTGT (01-1/GTGT & 01-2/GTGT)'

    date_from = fields.Date(
        string='Từ ngày',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )
    date_to = fields.Date(
        string='Đến ngày',
        required=True,
        default=fields.Date.context_today
    )
    company_id = fields.Many2one(
        'res.company',
        string='Công ty',
        required=True,
        default=lambda self: self.env.company
    )
    report_type = fields.Selection(
        [
            ('outbound', 'Bảng kê Bán ra (Mẫu 01-1/GTGT)'),
            ('inbound', 'Bảng kê Mua vào (Mẫu 01-2/GTGT)'),
            ('all', 'Cả hai bảng kê (Mua vào & Bán ra)'),
        ],
        string='Loại bảng kê',
        required=True,
        default='all'
    )
    state_filter = fields.Selection(
        [
            ('posted', 'Chỉ hóa đơn Đã vào sổ (Posted)'),
            ('all', 'Tất cả (Bao gồm Nháp & Đã vào sổ)'),
        ],
        string='Trạng thái chứng từ',
        default='posted',
        required=True
    )

    def action_print_pdf(self):
        """Xuất file PDF Bảng kê Thuế GTGT"""
        self.ensure_one()
        return self.env.ref('l10n_vn_vat_declaration.action_report_vat_declaration').report_action(self)

    def action_view_invoices(self):
        """Xem danh sách hóa đơn theo kỳ kê khai ngay trên màn hình"""
        self.ensure_one()
        domain = [
            ('company_id', '=', self.company_id.id),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ]
        if self.state_filter == 'posted':
            domain.append(('state', '=', 'posted'))

        if self.report_type == 'outbound':
            domain.append(('move_type', 'in', ('out_invoice', 'out_refund')))
        elif self.report_type == 'inbound':
            domain.append(('move_type', 'in', ('in_invoice', 'in_refund')))
        else:
            domain.append(('move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')))

        return {
            'name': _('Hóa đơn trong kỳ kê khai thuế (%s - %s)') % (self.date_from, self.date_to),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'default_company_id': self.company_id.id},
        }

    def get_vat_data(self):
        """Hàm chuẩn bị dữ liệu chi tiết cho QWeb template xuất PDF"""
        self.ensure_one()
        Move = self.env['account.move']
        base_domain = [
            ('company_id', '=', self.company_id.id),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ]
        if self.state_filter == 'posted':
            base_domain.append(('state', '=', 'posted'))

        out_lines = []
        in_lines = []

        if self.report_type in ('outbound', 'all'):
            out_moves = Move.search(base_domain + [('move_type', 'in', ('out_invoice', 'out_refund'))], order='invoice_date asc, name asc')
            for m in out_moves:
                sign = -1 if m.move_type == 'out_refund' else 1
                out_lines.append({
                    'name': m.name or '',
                    'ref': m.ref or '',
                    'date': m.invoice_date,
                    'partner_name': m.partner_id.name or '',
                    'partner_vat': m.partner_id.vat or '',
                    'untaxed_amount': m.amount_untaxed * sign,
                    'tax_amount': m.amount_tax * sign,
                    'total_amount': m.amount_total * sign,
                    'state': m.state,
                })

        if self.report_type in ('inbound', 'all'):
            in_moves = Move.search(base_domain + [('move_type', 'in', ('in_invoice', 'in_refund'))], order='invoice_date asc, name asc')
            for m in in_moves:
                sign = -1 if m.move_type == 'in_refund' else 1
                in_lines.append({
                    'name': m.name or '',
                    'ref': m.ref or '',
                    'date': m.invoice_date,
                    'partner_name': m.partner_id.name or '',
                    'partner_vat': m.partner_id.vat or '',
                    'untaxed_amount': m.amount_untaxed * sign,
                    'tax_amount': m.amount_tax * sign,
                    'total_amount': m.amount_total * sign,
                    'state': m.state,
                })

        return {
            'outbound': out_lines,
            'inbound': in_lines,
            'total_out_untaxed': sum(x['untaxed_amount'] for x in out_lines),
            'total_out_tax': sum(x['tax_amount'] for x in out_lines),
            'total_in_untaxed': sum(x['untaxed_amount'] for x in in_lines),
            'total_in_tax': sum(x['tax_amount'] for x in in_lines),
        }
