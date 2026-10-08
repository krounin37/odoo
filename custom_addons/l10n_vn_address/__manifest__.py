# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Địa Giới Hành Chính 3 Cấp (Tỉnh - Huyện - Xã)',
    'version': '1.0.0',
    'category': 'Localization',
    'summary': 'Quản lý Quận/Huyện và Phường/Xã Việt Nam cho Khách hàng & Nhà cung cấp',
    'description': """
Quản lý địa giới hành chính Việt Nam 3 cấp:
===========================================
- Bổ sung danh mục Quận/Huyện/Thị xã (res.district) trực thuộc Tỉnh/Thành phố.
- Bổ sung danh mục Phường/Xã/Thị trấn (res.ward) trực thuộc Quận/Huyện.
- Tích hợp vào thông tin liên hệ (res.partner) với bộ lọc linh hoạt:
  + Chọn Tỉnh -> Tự lọc danh sách Huyện
  + Chọn Huyện -> Tự lọc danh sách Xã và tự điền Tỉnh
  + Chọn Xã -> Tự điền Huyện và Tỉnh
- Nút tự động chuẩn hóa và cập nhật chuỗi địa chỉ đầy đủ.
- Sẵn sàng tích hợp các đơn vị giao vận (GHN, GHTK, Viettel Post) và xuất hóa đơn điện tử.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/res_country_data.xml',
        'data/res_country_state_new_data.xml',
        'data/res_district_data.xml',
        'views/res_district_views.xml',
        'views/res_ward_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
