# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Quản Lý Thuế TNCN & Bảo Hiểm Xã Hội (PIT & Social Insurance)',
    'version': '1.0.0',
    'category': 'Human Resources/Localizations',
    'summary': 'Quản lý CCCD, MST cá nhân, mã sổ BHXH, số người phụ thuộc và công cụ tính Thuế TNCN lũy tiến 7 bậc / Lương Gross - Net',
    'description': """
Quản lý Thuế TNCN và Bảo hiểm theo Luật Lao Động & Luật Thuế TNCN Việt Nam:
==========================================================================
- Quản lý thông tin định danh người lao động:
  + Số Căn cước công dân (CCCD / CMND)
  + Mã số thuế thu nhập cá nhân (MST)
  + Số sổ Bảo hiểm xã hội (BHXH)
  + Số người phụ thuộc giảm trừ gia cảnh
- Tự động tính toán các khoản trích đóng bảo hiểm bắt buộc:
  + Người lao động đóng: BHXH (8%), BHYT (1.5%), BHTN (1%) -> Tổng 10.5%
  + Doanh nghiệp đóng: BHXH (17.5%), BHYT (3%), BHTN (1%), KPCĐ (2%) -> Tổng 23.5%
  + Áp dụng trần đóng BHXH/BHYT (20 lần mức lương cơ sở)
- Tự động tính Thuế Thu Nhập Cá Nhân (TNCN):
  + Áp dụng mức giảm trừ gia cảnh (Bản thân: 11 triệu/tháng, Người phụ thuộc: 4.4 triệu/người/tháng)
  + Tính chuẩn xác theo biểu thuế lũy tiến từng phần 7 bậc (Thông tư 111/2013/TT-BTC)
- Mô phỏng và tính toán tức thì Lương Gross -> Lương Net thực nhận ngay trên hồ sơ nhân viên.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['base', 'hr'],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
