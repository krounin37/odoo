# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Tích Hợp Đơn Vị Giao Vận Giao Hàng Tiết Kiệm (GHTK)',
    'version': '1.0.0',
    'category': 'Inventory/Delivery',
    'summary': 'Tự động tính cước, đẩy đơn vận chuyển và in tem nhãn Giao Hàng Tiết Kiệm (GHTK)',
    'description': """
Tích hợp Đơn Vị Giao Hàng Tiết Kiệm (GHTK) với Odoo:
===================================================
- Tự động tính cước vận chuyển dự tính trên Báo giá & Đơn hàng bán dựa theo Địa chỉ người nhận và khối lượng hàng.
- Đẩy đơn giao vận tự động sang GHTK từ Phiếu xuất kho (stock.picking):
  + Tự động truyền thông tin người nhận, tiền thu hộ COD, địa chỉ 3 cấp (kết hợp l10n_vn_address).
  + Nhận về Mã vận đơn (Tracking Code) chính thức từ GHTK.
  + Hỗ trợ in nhãn vận đơn A6/A7 dán trực tiếp lên kiện hàng.
- Tự động tra cứu và đồng bộ hành trình đơn hàng thời gian thực.
- Hỗ trợ chế độ Thử nghiệm (Staging) và Chạy thực tế (Production).
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['delivery', 'stock', 'sale', 'l10n_vn_address'],
    'data': [
        'views/delivery_carrier_views.xml',
        'views/stock_picking_views.xml',
        'data/delivery_ghtk_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
