# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Cơ Cấu Tổ Chức Phòng Ban & Quy Trình Doanh Nghiệp Chuẩn',
    'version': '1.0.0',
    'category': 'Human Resources/Localizations',
    'summary': 'Thiết lập sẵn sơ đồ cây 15 phòng ban, 32 chức danh vị trí và quy trình vận hành doanh nghiệp chuẩn trong Odoo',
    'description': """
Cơ Cấu Tổ Chức & Quy Trình Vận Hành Doanh Nghiệp Chuẩn Việt Nam:
==============================================================
- Thiết lập sẵn cây sơ đồ 15 phòng ban phân cấp rõ ràng theo mô hình doanh nghiệp hiện đại:
  1. Ban Giám Đốc (CEO, COO)
  2. Khối Kinh Doanh & Tiếp Thị:
     + Phòng Kinh Doanh (Sales)
     + Phòng Marketing
     + Phòng Chăm Sóc Khách Hàng (Customer Service)
  3. Khối Tài Chính - Kế Toán:
     + Phòng Kế Toán (Kế toán trưởng, Kế toán bán hàng, Kế toán mua hàng, Kế toán thuế, Kế toán kho)
  4. Khối Vận Hành & Chuỗi Cung Ứng:
     + Phòng Mua Hàng (Procurement & Purchasing)
     + Phòng Quản Lý Kho & Giao Vận (Inventory & Logistics)
  5. Khối Hành Chính - Nhân Sự:
     + Phòng Nhân Sự (HR, C&B, Tuyển dụng)
     + Phòng Hành Chính - Quản Trị
  6. Phòng Công Nghệ Thông Tin (IT & Systems)
- Thiết lập sẵn 32 vị trí chức danh công việc (hr.job) liên kết tương ứng.
- Tài liệu hóa quy trình chuẩn vận hành khép kín liên phòng ban: Bán hàng (Order-to-Cash), Mua hàng (Procure-to-Pay), Kho vận & Giao hàng, Kế toán tài chính, Nhân sự & Tiền lương.
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['hr'],
    'data': [
        'data/hr_department_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
