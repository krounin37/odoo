# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - In Phiếu Nhập Kho (01-VT) & Phiếu Xuất Kho (02-VT) Chuẩn Bộ Tài Chính',
    'version': '1.0.0',
    'category': 'Inventory/Localizations',
    'summary': 'In Phiếu Nhập Kho và Phiếu Xuất Kho theo đúng Mẫu 01-VT & 02-VT Thông tư 200/2014/TT-BTC của Bộ Tài Chính',
    'description': """
Mẫu in Phiếu Nhập Kho & Xuất Kho chuẩn Thông tư 200/2014/TT-BTC:
===============================================================
- Xuất file PDF Phiếu Nhập Kho (Mẫu số 01 - VT) cho các phiếu nhập hàng (Incoming/Receipts).
- Xuất file PDF Phiếu Xuất Kho (Mẫu số 02 - VT) cho các phiếu xuất hàng (Delivery/Outgoing).
- Đầy đủ thông tin pháp lý chứng từ kế toán vật tư:
  + Tên công ty, bộ phận, địa chỉ, mã số thuế.
  + Tiêu đề chứng từ, ngày tháng năm, số phiếu.
  + Định khoản kế toán Nợ / Có.
  + Họ và tên người giao hàng / người nhận hàng.
  + Tên kho nhập/xuất, địa điểm kho.
  + Bảng chi tiết vật tư, mã hàng, đơn vị tính, số lượng theo chứng từ / thực nhập / thực xuất, đơn giá, thành tiền.
  + Tổng số tiền bằng chữ (tích hợp l10n_vn_amount_to_text).
  + Kèm theo chứng từ gốc.
  + 5 chữ ký đầy đủ theo mẫu BTC: Giám đốc / Thủ trưởng đơn vị, Kế toán trưởng, Người giao/nhận hàng, Thủ kho, Người lập phiếu.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['stock', 'l10n_vn', 'l10n_vn_amount_to_text'],
    'data': [
        'views/stock_picking_views.xml',
        'report/ir_actions_report.xml',
        'report/report_stock_receipt_templates.xml',
        'report/report_stock_delivery_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
