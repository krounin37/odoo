# Module Odoo: Cổng Thanh Toán Trực Tuyến VNPAY (payment_vnpay)

Module tích hợp cổng thanh toán trực tuyến hàng đầu Việt Nam - **VNPAY** (phiên bản chuẩn v2.1.0) cho Odoo Website, eCommerce và Cổng thanh toán hóa đơn khách hàng (Portal Invoice).

### 🌟 Tính năng chính:
- **Phương thức thanh toán toàn diện**:
  - **VNPAY-QR**: Quét mã thanh toán trực tiếp qua hơn 35 ứng dụng ngân hàng và ví điện tử hàng đầu tại Việt Nam.
  - **Thẻ ATM nội địa**: Thanh toán trực tuyến qua 40+ ngân hàng Việt Nam.
  - **Thẻ thanh toán quốc tế**: Visa, MasterCard, JCB.
- **Tiêu chuẩn bảo mật VNPAY 2.1.0**:
  - Mã hóa và ký số bảo mật bằng thuật toán **HMAC-SHA512**.
  - Kiểm tra chữ ký an toàn 2 chiều giữa Odoo và hệ thống VNPAY.
- **Tự động hóa thanh toán 100%**:
  - Xử lý chuyển hướng **Return URL**: Đưa khách hàng trở lại trang kết quả đơn hàng ngay sau khi thanh toán.
  - Xử lý **IPN Webhook (Server-to-Server)**: Xác nhận giao dịch và chuyển trạng thái đơn hàng sang "Đã thanh toán" (Paid) tự động, ngay cả khi khách đóng trình duyệt trước khi redirect.
- **Hỗ trợ 2 chế độ**:
  - **Thử nghiệm (Sandbox / Test)**: Sử dụng cấu hình mẫu sẵn có để test luồng thanh toán mà không phát sinh chi phí thật.
  - **Chính thức (Production / Live)**: Chỉ cần điền TMN Code và Hash Secret do VNPAY ký hợp đồng cấp.

### 🚀 Hướng dẫn kích hoạt & Cấu hình:
1. Vào menu **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm kiếm `payment_vnpay` hoặc `VNPAY` và bấm **Activate (Cài đặt)**.
3. Vào **Invoicing / Accounting > Configuration > Payment Providers (Phương thức thanh toán)**.
4. Mở phương thức **VNPAY**:
   - Chọn trạng thái **Test** (hoặc **Enabled** khi chạy thật).
   - Nhập **TMN Code** (Mã website) và **Hash Secret** (Chuỗi bí mật).
   - Bấm **Save** và xuất bản (**Publish** trên website).
5. Khi khách hàng mua hàng tại giỏ hàng (`/shop/cart`) hoặc thanh toán hóa đơn trên Portal, tùy chọn **VNPAY** sẽ hiển thị sẵn sàng.
