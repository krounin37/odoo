# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Tự động tra cứu Mã Số Thuế Doanh Nghiệp',
    'version': '1.0.0',
    'category': 'Localization',
    'summary': 'Tự động tra cứu tên công ty, địa chỉ và trạng thái hoạt động qua Mã số thuế từ dữ liệu Tổng cục Thuế',
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
