# Module Odoo: Tích Hợp Hóa Đơn Điện Tử MISA meInvoice (l10n_vn_edi_misa)

Module kết nối API chính thức của MISA meInvoice, hỗ trợ doanh nghiệp Việt Nam phát hành hóa đơn điện tử trực tiếp từ Hóa đơn khách hàng Odoo chỉ bằng 1 click.

### 🌟 Tính năng chính:
- **Cấu hình kết nối API linh hoạt (Settings)**:
  - Máy chủ MISA API URL (Mặc định: `https://meinvoiceapi.misa.vn`).
  - Mã số thuế công ty bên bán.
  - App ID, Tài khoản & Mật khẩu đăng nhập MISA.
  - Mẫu số hóa đơn (Template Code) và Ký hiệu hóa đơn (Series) theo đăng ký với cơ quan thuế.
- **Phát hành hóa đơn 1-Click (1-Click Publish)**:
  - Nút **"Phát hành MISA meInvoice"** trực tiếp trên thanh công cụ của Hóa đơn khách hàng (`account.move`).
  - Tự động đóng gói chi tiết các dòng sản phẩm, đơn giá, số lượng, thuế suất GTGT (0%, 5%, 8%, 10%, không chịu thuế) và thông tin đối tác người mua.
  - Hỗ trợ chế độ **Sandbox / Thử nghiệm** (khi chưa điền tài khoản MISA thật) để kiểm thử luồng phát hành an toàn.
- **Đồng bộ trạng thái & Tra cứu tức thì**:
  - Tự động lưu **Số hóa đơn điện tử chính thức** và **Mã tra cứu hóa đơn** do MISA cấp.
  - Nút **"Xem HĐ MISA Online"**: Mở ngay liên kết tra cứu hóa đơn trực tuyến trên website của MISA để tải về file PDF/XML hóa đơn gốc đã ký số.
  - Thẻ trạng thái MISA hiển thị trực quan (Chưa phát hành / Đã phát hành & Ký số / Đã hủy).

### 🚀 Cách kích hoạt trong Odoo:
1. Vào **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm `l10n_vn_edi_misa` hoặc `MISA` và bấm **Activate (Cài đặt)**.
3. Vào **Accounting (Kế toán) > Configuration > Settings > Hóa Đơn Điện Tử MISA meInvoice** để cấu hình tài khoản.
4. Mở một Hóa đơn khách hàng đã vào sổ (Posted) và bấm nút **Phát hành MISA meInvoice**.
