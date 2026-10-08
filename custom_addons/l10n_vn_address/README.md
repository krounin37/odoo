# Module Odoo: Quản Lý Địa Giới Hành Chính 3 Cấp Việt Nam (l10n_vn_address)

Module bổ sung phân cấp địa giới hành chính chuẩn Việt Nam (Tỉnh/Thành phố → Quận/Huyện → Phường/Xã) và mẫu địa chỉ hành chính mới cho Odoo.

### 🌟 Tính năng chính:
- **Bộ dữ liệu địa giới hành chính mới đầy đủ toàn quốc (Tổng cục Thống kê GSO & Bộ Nội vụ)**:
  - **63 Tỉnh / Thành phố trực thuộc Trung ương** (`res.country.state`).
  - **700+ Quận / Huyện / Thị xã / Thành phố trực thuộc tỉnh** (`res.district`) trên toàn bộ 63 tỉnh thành (bao gồm cả TP. Thủ Đức, các thành phố và thị xã mới được nâng cấp).
  - Phân cấp liên kết chặt chẽ: `res.ward` (Phường / Xã) thuộc `res.district` (Quận / Huyện) thuộc `res.country.state` (Tỉnh / Thành).
- **Mẫu hiển thị & Nhập liệu địa chỉ chuẩn Việt Nam**:
  - Giao diện nhập thông tin liên hệ được tối ưu riêng cho Việt Nam:
    + `street`: Số nhà, ngõ/ngách, tên đường, tòa nhà.
    + `ward_id`: Phường / Xã / Thị trấn (tự động lọc theo Quận/Huyện).
    + `district_id`: Quận / Huyện / Thị xã / TP thuộc tỉnh (tự động lọc theo Tỉnh/Thành).
    + `state_id`: Tỉnh / Thành phố.
    + `country_id`: Việt Nam.
  - Tự động ẩn các ô không sử dụng ở Việt Nam như `street2`, `zip` khi quốc gia là Việt Nam.
- **Tự động lọc và đồng bộ thông minh trên Danh bạ (res.partner)**:
  - Chọn Tỉnh → Tự động lọc danh sách Quận/Huyện thuộc Tỉnh đó.
  - Chọn Huyện → Tự động lọc Phường/Xã và tự động điền Tỉnh.
  - Chọn Xã → Tự động điền Huyện và Tỉnh.
  - Đồng bộ tự động vào trường chuẩn `city` của Odoo để tương thích 100% với các module eCommerce, Invoicing và Delivery.
- **Chuẩn hóa địa chỉ tự động**:
  - Nút **"Chuẩn hóa chuỗi địa chỉ"** giúp ghép nhanh: `[Số nhà/Tên đường], [Phường/Xã], [Quận/Huyện], [Tỉnh/Thành phố]`.
  - Phù hợp tuyệt đối khi xuất hóa đơn điện tử VAT và tích hợp bàn giao vận chuyển (GHN, GHTK, Viettel Post).

### 🚀 Cách kích hoạt trong Odoo:
1. Vào **Apps** (Ứng dụng).
2. Bật chế độ Nhà phát triển (**Developer Mode**).
3. Bấm **Update Apps List** (Cập nhật danh sách ứng dụng).
4. Tìm kiếm từ khóa `l10n_vn_address` hoặc `Địa Giới` và bấm **Activate (Cài đặt)**.
5. Quản lý danh mục tại: **Contacts (Danh bạ) > Configuration (Cấu hình) > Localization > Quận / Huyện & Phường / Xã**.
