# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Bảng Kê Thuế GTGT Mua Vào & Bán Ra (Mẫu 01-1/GTGT & 01-2/GTGT)',
    'version': '1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Kết xuất Bảng kê Hóa đơn Mua vào và Bán ra phục vụ đối chiếu thuế GTGT và nhập phần mềm HTKK Tổng cục Thuế',
    'description': """
Báo cáo Bảng Kê Thuế GTGT Chuẩn Tổng Cục Thuế Việt Nam:
======================================================
- Bảng kê hóa đơn, chứng từ hàng hóa dịch vụ Bán ra (Mẫu số 01-1/GTGT):
  + Phân nhóm theo thuế suất: Không chịu thuế, 0%, 5%, 8%, 10%.
  + Đầy đủ thông tin: Ký hiệu, số hóa đơn, ngày lập, tên khách hàng, mã số thuế, doanh số chưa thuế, tiền thuế GTGT.
- Bảng kê hóa đơn, chứng từ hàng hóa dịch vụ Mua vào (Mẫu số 01-2/GTGT):
  + Tổng hợp hóa đơn mua vào trong kỳ.
  + Doanh số mua chưa thuế, thuế suất và tiền thuế GTGT được khấu trừ.
- Hỗ trợ xem trực quan trên giao diện Odoo và xuất file báo cáo PDF/Excel phục vụ kê khai thuế hàng tháng hoặc hàng quý.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['account', 'l10n_vn'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/vat_declaration_wizard_views.xml',
        'report/ir_actions_report.xml',
        'report/report_vat_declaration_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
