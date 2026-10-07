# -*- coding: utf-8 -*-
{
    'name': 'Vietnam - Cổng Thanh Toán Trực Tuyến VNPAY',
    'version': '1.0.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 360,
    'summary': 'Tích hợp cổng thanh toán trực tuyến VNPAY (VNPAY-QR, Thẻ ATM nội địa, Thẻ quốc tế Visa/Mastercard)',
    'description': """
Cổng thanh toán điện tử VNPAY (v2.1.0):
======================================
- Hỗ trợ thanh toán trực tuyến cho Website Bán hàng (eCommerce), Cổng thanh toán hóa đơn khách hàng (Portal Invoice).
- Phương thức thanh toán đa dạng:
  + VNPAY-QR (quét mã qua 30+ ứng dụng ngân hàng và ví điện tử)
  + Thẻ ATM & Tài khoản ngân hàng nội địa
  + Thẻ quốc tế (Visa, Master, JCB)
- Cơ chế bảo mật và đồng bộ:
  + Mã hóa và xác thực chữ ký an toàn HMAC-SHA512 chuẩn VNPAY 2.1.0
  + Xử lý Callback chuyển hướng (Return URL)
  + Xử lý Webhook tức thì Server-to-Server (IPN) tự động cập nhật trạng thái đơn hàng và hóa đơn ngay khi khách thanh toán thành công.
- Hỗ trợ cả môi trường Thử nghiệm (Sandbox) và Môi trường thực tế (Production).
    """,
    'author': 'krounin37',
    'website': 'https://github.com/krounin37/odoo',
    'license': 'LGPL-3',
    'depends': ['payment'],
    'data': [
        'views/payment_vnpay_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
