# -*- coding: utf-8 -*-
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_preview_sale_order(self):
        """Mở xem trước trực tiếp bản in PDF A4 chuẩn của Báo giá / Đơn hàng trên tab mới của trình duyệt"""
        self.ensure_one()
        report = self.env.ref('sale.action_report_saleorder', raise_if_not_found=False)
        report_name = report.report_name if report else 'sale.report_saleorder'
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/pdf/{report_name}/{self.id}',
            'target': 'new',
        }


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_preview_purchase_order(self):
        """Mở xem trước trực tiếp bản in PDF A4 chuẩn của Đơn mua hàng trên tab mới của trình duyệt"""
        self.ensure_one()
        report = self.env.ref('purchase.action_report_purchase_order', raise_if_not_found=False)
        report_name = report.report_name if report else 'purchase.report_purchaseorder'
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/pdf/{report_name}/{self.id}',
            'target': 'new',
        }


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_preview_invoice(self):
        """Mở xem trước trực tiếp bản in PDF A4 chuẩn của Hóa đơn trên tab mới của trình duyệt"""
        self.ensure_one()
        report = self.env.ref('account.account_invoices', raise_if_not_found=False)
        report_name = report.report_name if report else 'account.report_invoice'
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/pdf/{report_name}/{self.id}',
            'target': 'new',
        }


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_preview_stock_voucher(self):
        """Mở xem trước trực tiếp bản in PDF A4 chuẩn của Phiếu nhập kho (01-VT) hoặc Phiếu xuất kho (02-VT) theo TT200 trên tab mới"""
        self.ensure_one()
        if self.picking_type_id.code == 'incoming':
            report = self.env.ref('l10n_vn_stock_voucher.action_report_stock_receipt_vn', raise_if_not_found=False)
            report_name = report.report_name if report else 'l10n_vn_stock_voucher.report_stock_receipt_document_vn'
        else:
            report = self.env.ref('l10n_vn_stock_voucher.action_report_stock_delivery_vn', raise_if_not_found=False)
            report_name = report.report_name if report else 'l10n_vn_stock_voucher.report_stock_delivery_document_vn'
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/pdf/{report_name}/{self.id}',
            'target': 'new',
        }


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_preview_cash_voucher(self):
        """Mở xem trước trực tiếp bản in PDF A4 chuẩn của Phiếu Thu (01-TT) hoặc Phiếu Chi (02-TT) theo TT200 trên tab mới"""
        self.ensure_one()
        if self.payment_type == 'inbound':
            report = self.env.ref('l10n_vn_cash_voucher.action_report_cash_receipt_vn', raise_if_not_found=False)
            report_name = report.report_name if report else 'l10n_vn_cash_voucher.report_cash_receipt_document_vn'
        else:
            report = self.env.ref('l10n_vn_cash_voucher.action_report_cash_payment_vn', raise_if_not_found=False)
            report_name = report.report_name if report else 'l10n_vn_cash_voucher.report_cash_payment_document_vn'
        return {
            'type': 'ir.actions.act_url',
            'url': f'/report/pdf/{report_name}/{self.id}',
            'target': 'new',
        }
