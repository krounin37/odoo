# Module Odoo: Tra Cứu Mã Số Thuế Doanh Nghiệp Việt Nam (l10n_vn_tax_lookup)

Module hỗ trợ doanh nghiệp Việt Nam tự động tra cứu dữ liệu từ Tổng cục Thuế thông qua API mở tốc độ cao.

### 🌟 Tính năng chính:
- Thêm nút **Tra cứu MST** ngay cạnh trường Mã số thuế (`vat`) của Khách hàng / Nhà cung cấp (`res.partner`).
- Tự động điền:
  - **Tên công ty**: Tên pháp nhân đầy đủ theo đăng ký kinh doanh.
  - **Địa chỉ kinh doanh**: Địa chỉ trụ sở chính đã đăng ký với chi cục thuế.
  - **Tên giao dịch quốc tế**: Tên tiếng Anh.
  - **Tên viết tắt**: Tên viết tắt của công ty.
  - **Trạng thái thuế**: Kiểm tra doanh nghiệp đang "NNT đang hoạt động" hay đã tạm ngừng / giải thể (tránh rủi ro xuất hóa đơn sai).
- Tự động chuyển đối tác sang dạng **Company** (`is_company = True`).

### 🚀 Cách kích hoạt trong Odoo:
1. Vào menu **Apps** (Ứng dụng).
2. Bật chế độ Nhà phát triển (**Developer Mode**).
3. Bấm **Update Apps List** (Cập nhật danh sách ứng dụng).
4. Tìm kiếm từ khóa `l10n_vn_tax_lookup` hoặc `Mã Số Thuế` và bấm **Activate (Cài đặt)**.
