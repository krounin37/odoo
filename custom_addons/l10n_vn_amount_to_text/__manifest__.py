# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Đọc Số Tiền Thành Chữ Tiếng Việt (VAS/BTC)',
    'version': '1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Tự động chuyển đổi số tiền thành chữ bằng Tiếng Việt trên Hóa đơn, Báo giá và Phiếu thu chi',
    'description': """
Chuyển đổi số tiền thành chữ chuẩn quy tắc ngữ pháp Tiếng Việt:
=============================================================
- Tuân thủ quy định Luật Kế toán Việt Nam về thể hiện số tiền bằng chữ trên chứng từ kế toán.
- Xử lý hoàn hảo các quy tắc đọc:
  + "mười một", "hai mươi mốt"
  + "mười lăm", "ba mươi lăm"
  + "lẻ" / "linh" (ví dụ: một trăm linh năm)
  + Đơn vị tiền tệ (đồng, xu, USD, EUR...)
- Tích hợp sẵn trên:
  + Hóa đơn khách hàng & Nhà cung cấp (account.move)
  + Phiếu thanh toán / Phiếu thu chi (account.payment)
  + Báo giá & Đơn bán hàng (sale.order)
- Kế thừa mẫu in Hóa đơn PDF hiển thị dòng "Số tiền bằng chữ: ... đồng chẵn."
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['account', 'sale', 'l10n_vn'],
    'data': [
        'views/account_move_views.xml',
        'report/report_invoice_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
