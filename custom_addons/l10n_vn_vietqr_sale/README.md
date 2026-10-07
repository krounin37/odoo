# Module Odoo: VietQR Trên Báo Giá & Đơn Bán Hàng (l10n_vn_vietqr_sale)

Module hỗ trợ doanh nghiệp Việt Nam tự động sinh mã VietQR động NAPAS 247 trên Báo giá (Quotation) và Đơn bán hàng (Sale Order).

### 🌟 Tính năng chính:
- **Tự động sinh mã VietQR động**:
  - Gắn đúng thông tin tài khoản ngân hàng của công ty.
  - Tự động điền số tiền (`amount_total`) theo đơn hàng.
  - Tự động gán nội dung chuyển tiền (cú pháp: `<Mã đơn hàng> thanh toan`).
  - Hỗ trợ hầu hết các ngân hàng lớn tại Việt Nam (Vietcombank, MB, Techcombank, VietinBank, BIDV, ACB, VPBank, TPBank, Sacombank,...).
- **Hiển thị trực quan**:
  - Tab "Thanh Toán VietQR" ngay trong giao diện Đơn hàng bán.
  - Nút "Làm mới mã QR" để cập nhật lại khi thay đổi giá trị đơn hàng hoặc số tài khoản.
- **Tích hợp trên mẫu in PDF**:
  - Khung thanh toán VietQR chuyên nghiệp, hiển thị số tài khoản thụ hưởng và hình ảnh mã QR ở chân trang báo giá/đơn hàng, giúp khách hàng quét chuyển khoản nhanh chóng.

### 🚀 Cách kích hoạt trong Odoo:
1. Vào **Apps** (Ứng dụng).
2. Bật chế độ Nhà phát triển (**Developer Mode**).
3. Bấm **Update Apps List** (Cập nhật danh sách ứng dụng).
4. Tìm kiếm từ khóa `l10n_vn_vietqr_sale` hoặc `VietQR` và bấm **Activate (Cài đặt)**.
5. Cấu hình số tài khoản ngân hàng công ty trong **Contacts > Công ty của bạn > Invoicing/Bank Accounts** (điền số tài khoản và chọn ngân hàng).
