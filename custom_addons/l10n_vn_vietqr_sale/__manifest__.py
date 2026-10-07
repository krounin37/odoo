# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - VietQR trên Báo giá & Đơn Bán Hàng',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Tự động tạo mã VietQR động kèm số tiền và nội dung đơn hàng trên Báo giá & Đơn bán hàng',
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['sale', 'account', 'l10n_vn'],
    'data': [
        'views/res_partner_bank_views.xml',
        'views/sale_order_views.xml',
        'report/sale_order_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
