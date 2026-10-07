# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Tích Hợp Hóa Đơn Điện Tử MISA meInvoice',
    'version': '1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'Tự động phát hành, ký số và đồng bộ Hóa đơn điện tử MISA meInvoice từ Hóa đơn Odoo',
    'description': """
Tích hợp Hóa đơn điện tử MISA meInvoice với Odoo:
=================================================
- Cấu hình thông tin kết nối API MISA meInvoice trong Cài đặt (App ID, Mã số thuế, Tài khoản, Mật khẩu, Mẫu số, Ký hiệu).
- Phát hành hóa đơn trực tiếp từ Hóa đơn khách hàng (account.move) chỉ bằng 1 click.
- Tự động đóng gói dữ liệu chi tiết hàng hóa, thuế suất GTGT, thông tin người mua.
- Nhận về Mã tra cứu, Số hóa đơn điện tử chính thức và Link xem/tải hóa đơn gốc từ máy chủ MISA.
- Cập nhật trạng thái ký số và đồng bộ dữ liệu hóa đơn điện tử tự động.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['account', 'l10n_vn'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
