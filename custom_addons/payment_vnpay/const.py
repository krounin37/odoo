# -*- coding: utf-8 -*-

SUPPORTED_CURRENCIES = ['VND']

VNPAY_SANDBOX_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNPAY_PROD_URL = 'https://pay.vnpay.vn/vpcpay.html'

RESPONSE_CODES = {
    '00': 'Giao dịch thành công',
    '07': 'Trừ tiền thành công. Giao dịch bị nghi ngờ (liên quan tới lừa đảo, bất thường).',
    '09': 'Giao dịch không thành công do thẻ/tài khoản chưa đăng ký dịch vụ InternetBanking.',
    '10': 'Giao dịch không thành công do xác thực thông tin thẻ/tài khoản sai quá 3 lần.',
    '11': 'Giao dịch không thành công do đã hết hạn chờ thanh toán.',
    '12': 'Giao dịch không thành công do thẻ/tài khoản bị khóa.',
    '13': 'Giao dịch không thành công do nhập sai mật khẩu OTP.',
    '24': 'Giao dịch không thành công do khách hàng đã hủy giao dịch.',
    '51': 'Giao dịch không thành công do tài khoản không đủ số dư.',
    '65': 'Giao dịch không thành công do vượt quá hạn mức giao dịch trong ngày.',
    '75': 'Ngân hàng thanh toán đang bảo trì.',
    '79': 'Giao dịch không thành công do nhập sai mật khẩu quá số lần quy định.',
    '99': 'Lỗi không xác định khác từ hệ thống VNPAY.',
}
