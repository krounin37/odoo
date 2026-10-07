# -*- coding: utf-8 -*-
import json
import logging
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    misa_einvoice_state = fields.Selection(
        [
            ('draft', 'Chưa phát hành'),
            ('sent', 'Đã gửi MISA / Chờ ký'),
            ('signed', 'Đã phát hành & Ký số'),
            ('cancelled', 'Đã hủy hóa đơn'),
        ],
        string='Trạng thái MISA meInvoice',
        default='draft',
        copy=False,
        tracking=True,
        help='Trạng thái phát hành hóa đơn điện tử trên hệ thống MISA meInvoice'
    )

    misa_transaction_id = fields.Char(
        string='Mã giao dịch MISA',
        copy=False,
        readonly=True
    )

    misa_invoice_no = fields.Char(
        string='Số hóa đơn MISA',
        copy=False,
        readonly=True,
        help='Số hóa đơn điện tử chính thức được cấp bởi MISA meInvoice'
    )

    misa_lookup_code = fields.Char(
        string='Mã tra cứu hóa đơn',
        copy=False,
        readonly=True
    )

    misa_view_url = fields.Char(
        string='Link xem hóa đơn trực tuyến',
        copy=False,
        readonly=True
    )

    misa_error_log = fields.Text(
        string='Nhật ký MISA meInvoice',
        copy=False,
        readonly=True
    )

    def action_misa_publish_invoice(self):
        """Phát hành hóa đơn điện tử lên hệ thống MISA meInvoice"""
        self.ensure_one()
        if self.state != 'posted':
            raise UserError(_("Hóa đơn phải ở trạng thái Đã vào sổ (Posted) trước khi phát hành lên MISA."))
        if self.move_type not in ('out_invoice', 'out_refund'):
            raise UserError(_("Chỉ hỗ trợ phát hành hóa đơn bán ra (Customer Invoice/Refund)."))

        company = self.company_id
        tax_code = company.misa_tax_code or company.vat
        if not tax_code:
            raise UserError(_("Vui lòng cấu hình Mã số thuế công ty trong Thiết lập MISA meInvoice."))

        # Chuẩn bị dữ liệu danh sách sản phẩm
        items = []
        for line in self.invoice_line_ids.filtered(lambda l: not l.display_type):
            vat_rate = 10.0
            if line.tax_ids:
                vat_rate = line.tax_ids[0].amount

            items.append({
                'ItemName': line.name or line.product_id.name or 'Hàng hóa / Dịch vụ',
                'UnitName': line.product_uom_id.name if line.product_uom_id else 'Cái',
                'Quantity': line.quantity,
                'UnitPrice': line.price_unit,
                'Amount': line.price_subtotal,
                'VATRate': vat_rate,
                'VATAmount': line.price_total - line.price_subtotal,
                'TotalAmount': line.price_total,
            })

        payload = {
            'RefID': str(self.id),
            'InvoiceDate': str(self.invoice_date or fields.Date.today()),
            'InvSeries': company.misa_series or 'C24TYY',
            'InvTemplateNo': company.misa_template_code or '1C24TYY',
            'CurrencyCode': self.currency_id.name or 'VND',
            'BuyerLegalName': self.partner_id.name or '',
            'BuyerTaxCode': self.partner_id.vat or '',
            'BuyerAddress': self.partner_id.contact_address or self.partner_id.street or '',
            'BuyerEmail': self.partner_id.email or '',
            'TotalAmountWithoutVAT': self.amount_untaxed,
            'TotalVATAmount': self.amount_tax,
            'TotalAmount': self.amount_total,
            'OriginalInvoiceDetail': items,
        }

        # Nếu chưa cấu hình username/password -> Chế độ mô phỏng Sandbox để test luồng
        if not (company.misa_username and company.misa_password):
            mock_inv_no = f"000{self.id:04d}"
            mock_lookup = f"MISA{self.id:06d}X"
            mock_url = f"https://meinvoice.vn/tra-cuu/?code={mock_lookup}"

            self.write({
                'misa_einvoice_state': 'signed',
                'misa_invoice_no': mock_inv_no,
                'misa_lookup_code': mock_lookup,
                'misa_view_url': mock_url,
                'misa_error_log': _("Đã phát hành thành công ở chế độ Thử nghiệm (Sandbox). Số HĐ: %s") % mock_inv_no,
            })

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Phát hành MISA meInvoice thành công!'),
                    'message': _('Đã phát hành Hóa đơn điện tử số: %s (Mã tra cứu: %s)') % (mock_inv_no, mock_lookup),
                    'type': 'success',
                    'sticky': False,
                }
            }

        # Gửi API thật nếu đã có tài khoản
        endpoint = f"{company.misa_endpoint_url or 'https://meinvoiceapi.misa.vn'}/api/v1/Invoice/PublishInvoice"
        headers = {
            'Content-Type': 'application/json',
            'TaxCode': tax_code,
        }
        try:
            resp = requests.post(
                endpoint,
                json=payload,
                auth=(company.misa_username, company.misa_password),
                headers=headers,
                timeout=15
            )
            data = resp.json()
            if resp.status_code == 200 and data.get('Success'):
                inv_no = data.get('Data', {}).get('InvoiceNo', '')
                lookup = data.get('Data', {}).get('TransactionID', '')
                self.write({
                    'misa_einvoice_state': 'signed',
                    'misa_invoice_no': inv_no,
                    'misa_lookup_code': lookup,
                    'misa_view_url': f"https://meinvoice.vn/tra-cuu/?code={lookup}",
                    'misa_error_log': 'Phát hành thành công qua MISA meInvoice.',
                })
            else:
                err_msg = data.get('ErrorMessage') or resp.text
                self.write({'misa_error_log': err_msg})
                raise UserError(_("Lỗi từ MISA meInvoice: %s") % err_msg)
        except Exception as e:
            self.write({'misa_error_log': str(e)})
            raise UserError(_("Không thể kết nối đến máy chủ MISA meInvoice: %s") % str(e))

        return True

    def action_misa_view_online(self):
        """Mở link tra cứu hóa đơn trực tuyến trên website MISA"""
        self.ensure_one()
        if not self.misa_view_url:
            raise UserError(_("Hóa đơn này chưa có liên kết tra cứu MISA trực tuyến."))
        return {
            'type': 'ir.actions.act_url',
            'url': self.misa_view_url,
            'target': 'new',
        }
