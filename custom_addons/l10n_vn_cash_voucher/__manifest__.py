# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - In Phiếu Thu (01-TT) & Phiếu Chi (02-TT) Chuẩn Bộ Tài Chính',
    'version': '1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'In Phiếu Thu và Phiếu Chi theo đúng Mẫu 01-TT & 02-TT Thông tư 200/2014/TT-BTC của Bộ Tài Chính',
    'description': """
Mẫu in Phiếu Thu & Phiếu Chi chuẩn Thông tư 200/2014/TT-BTC:
===========================================================
- Xuất file PDF Phiếu Thu (Mẫu số 01 - TT) cho các khoản tiền vào (Inbound payment).
- Xuất file PDF Phiếu Chi (Mẫu số 02 - TT) cho các khoản tiền ra (Outbound payment).
- Đầy đủ thông tin pháp lý theo Luật Kế toán Việt Nam:
  + Đơn vị, địa chỉ, mã số thuế của công ty.
  + Tiêu đề chứng từ, ngày tháng năm, số hiệu chứng từ.
  + Định khoản kế toán Nợ / Có.
  + Họ và tên người nộp / nhận tiền, địa chỉ, lý do nộp / chi.
  + Số tiền bằng số và số tiền bằng chữ (tích hợp chuẩn l10n_vn_amount_to_text).
  + Kèm theo chứng từ gốc.
  + Đầy đủ 5 vị trí chữ ký chuẩn: Giám đốc, Kế toán trưởng, Người nộp/nhận, Người lập phiếu, Thủ quỹ.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['account', 'l10n_vn', 'l10n_vn_amount_to_text'],
    'data': [
        'views/account_payment_views.xml',
        'report/ir_actions_report.xml',
        'report/report_cash_receipt_templates.xml',
        'report/report_cash_payment_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
