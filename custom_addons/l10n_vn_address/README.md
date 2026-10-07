# Module Odoo: Quản Lý Địa Giới Hành Chính 3 Cấp Việt Nam (l10n_vn_address)

Module bổ sung phân cấp địa giới hành chính chuẩn Việt Nam (Tỉnh/Thành phố → Quận/Huyện → Phường/Xã) cho Odoo.

### 🌟 Tính năng chính:
- **Phân cấp 3 cấp**:
  - `res.country.state`: Tỉnh / Thành phố trực thuộc Trung ương (kế thừa từ Odoo base).
  - `res.district`: Quận / Huyện / Thị xã / Thành phố trực thuộc tỉnh.
  - `res.ward`: Phường / Xã / Thị trấn.
- **Tự động lọc và đồng bộ thông minh trên Danh bạ (res.partner)**:
  - Chọn Tỉnh → Tự động lọc danh sách Quận/Huyện thuộc Tỉnh đó.
  - Chọn Huyện → Tự động lọc Phường/Xã và tự động điền Tỉnh.
  - Chọn Xã → Tự động điền Huyện và Tỉnh.
- **Chuẩn hóa địa chỉ tự động**:
  - Nút **"Chuẩn hóa chuỗi địa chỉ"** giúp ghép nhanh: `[Số nhà/Tên đường], [Phường/Xã], [Quận/Huyện], [Tỉnh/Thành phố]`.
  - Phù hợp tuyệt đối khi xuất hóa đơn điện tử VAT và tích hợp bàn giao vận chuyển (GHN, GHTK, Viettel Post).
- **Dữ liệu mẫu nạp sẵn**:
  - Đã nạp sẵn danh mục các Quận/Huyện trọng điểm tại Hà Nội, TP. Hồ Chí Minh và Đà Nẵng.

### 🚀 Cách kích hoạt trong Odoo:
1. Vào **Apps** (Ứng dụng).
2. Bật chế độ Nhà phát triển (**Developer Mode**).
3. Bấm **Update Apps List** (Cập nhật danh sách ứng dụng).
4. Tìm kiếm từ khóa `l10n_vn_address` hoặc `Địa Giới` và bấm **Activate (Cài đặt)**.
5. Quản lý danh mục tại: **Contacts (Danh bạ) > Configuration (Cấu hình) > Localization > Quận / Huyện & Phường / Xã**.
