# Hướng dẫn Cài đặt & Chạy Dự án Odoo

<p align="center">
  <a href="README.md"><b>English</b></a> |
  <a href="README.vi.md"><b>Tiếng Việt</b></a> |
  <a href="README.zh.md"><b>简体中文</b></a>
</p>

---

## 📌 Tổng quan

Repository này chứa mã nguồn nền tảng **Odoo** ERP cùng cấu hình Docker giúp triển khai nhanh chóng và hỗ trợ phát triển local.

---

## 🚀 Cách 1: Chạy nhanh bằng Docker (Khuyên dùng)

Cách đơn giản và ổn định nhất để khởi chạy Odoo kèm cơ sở dữ liệu PostgreSQL là sử dụng **Docker Compose**.

### Yêu cầu cài đặt
- Đã cài đặt và bật [Docker](https://docs.docker.com/get-docker/) (hoặc Docker Desktop).
- [Docker Compose](https://docs.docker.com/compose/install/) (đã tích hợp sẵn trên Docker Desktop).

### 1. Khởi động dịch vụ
Chạy lệnh sau tại thư mục gốc của dự án:

```bash
docker compose up -d
```

Lệnh trên sẽ khởi chạy 2 container:
- **web**: Dịch vụ web Odoo lắng nghe ở cổng `8069`.
- **db**: Máy chủ cơ sở dữ liệu PostgreSQL 16.

### 2. Truy cập hệ thống
Mở trình duyệt web và truy cập địa chỉ:
```
http://localhost:8069
```

Ở lần truy cập đầu tiên, điền biểu mẫu tạo cơ sở dữ liệu:
- **Master Password**: Mật khẩu quản trị DB (lưu giữ cẩn thận để backup/restore/xóa database).
- **Database Name**: Tên database (ví dụ: `odoo_db`).
- **Email / Password**: Tài khoản và mật khẩu quản trị viên đăng nhập Odoo.
- **Language / Country**: Chọn ngôn ngữ (Tiếng Việt) và quốc gia (Việt Nam).
- **Demo data**: Tích chọn nếu muốn nạp sẵn dữ liệu mẫu để thử nghiệm.

### 3. Các lệnh Docker hữu ích

- **Xem log dịch vụ web theo thời gian thực**:
  ```bash
  docker compose logs -f web
  ```
- **Dừng các container**:
  ```bash
  docker compose down
  ```
- **Dừng và xóa toàn bộ dữ liệu (reset database)**:
  ```bash
  docker compose down -v
  ```
- **Khởi động lại các container**:
  ```bash
  docker compose restart
  ```

---

## 🛠️ Cách 2: Cài đặt và chạy trực tiếp bằng Python (Môi trường Dev)

Nếu bạn muốn chạy trực tiếp Odoo bằng môi trường Python cục bộ không qua Docker:

### Yêu cầu tiên quyết
- Python 3.10, 3.11 hoặc 3.12.
- PostgreSQL 14+ đã cài đặt và đang chạy dịch vụ.
- `wkhtmltopdf` (tùy chọn nhưng khuyến nghị để xuất báo cáo PDF chuẩn).

### 1. Tạo và kích hoạt môi trường ảo (Virtual Environment)

```bash
# Trên Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Trên Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Cài đặt các thư viện phụ thuộc

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Cấu hình người dùng cơ sở dữ liệu PostgreSQL
Tạo người dùng và database PostgreSQL:

```bash
createuser -s odoo
createdb -O odoo odoo_db
```

### 4. Tạo file cấu hình (`odoo.conf`)
Tạo file `odoo.conf` tại thư mục gốc dự án:

```ini
[options]
addons_path = addons
admin_passwd = admin_secret_password
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
http_port = 8069
```

### 5. Khởi chạy Odoo Server

```bash
# Sử dụng file cấu hình
python odoo-bin -c odoo.conf

# Hoặc khởi chạy trực tiếp qua tham số dòng lệnh
python odoo-bin --addons-path=addons -d odoo_db --db_user=odoo --db_password=odoo
```

---

## 💡 Các lệnh nhà phát triển thường dùng

- **Bật chế độ Developer (tự động reload code Python & tài nguyên assets)**:
  ```bash
  python odoo-bin -c odoo.conf --dev=all
  ```
- **Cài đặt một module mới**:
  ```bash
  python odoo-bin -c odoo.conf -d odoo_db -i <tên_module>
  ```
- **Cập nhật / nâng cấp một module**:
  ```bash
  python odoo-bin -c odoo.conf -d odoo_db -u <tên_module>
  ```

---

## 🇻🇳 Bộ Module Bản Địa Hóa Việt Nam (`custom_addons/`)

Repository này đã được xây dựng và tích hợp sẵn bộ 3 module chuyên dụng cho thị trường và doanh nghiệp Việt Nam:

| Module | Tên & Tính Năng | Trạng Thái |
| :--- | :--- | :---: |
| **`l10n_vn_tax_lookup`** | **Tự động tra cứu Mã Số Thuế**: Tra cứu trực tiếp từ Tổng cục Thuế để tự động điền Tên công ty pháp nhân, địa chỉ kinh doanh và kiểm tra trạng thái hoạt động của doanh nghiệp khi nhập MST. | ✅ Sẵn sàng |
| **`l10n_vn_vietqr_sale`** | **Mã VietQR trên Báo giá & Đơn bán hàng**: Tự động sinh mã VietQR NAPAS 247 kèm số tiền chính xác và nội dung đơn hàng, hiển thị trên giao diện và in ra file PDF báo giá để khách hàng chuyển khoản tức thì. | ✅ Sẵn sàng |
| **`l10n_vn_address`** | **Địa giới hành chính 3 cấp**: Quản lý Quận/Huyện và Phường/Xã Việt Nam với cơ chế lọc liên hoàn thông minh và nút tự động chuẩn hóa địa chỉ phục vụ giao vận (GHN, GHTK, Viettel Post) & xuất hóa đơn VAT. | ✅ Sẵn sàng |
| **`l10n_vn_amount_to_text`** | **Đọc số tiền thành chữ Tiếng Việt**: Tự động chuyển đổi tổng tiền thành chữ Tiếng Việt chuẩn ngữ pháp và quy định chứng từ kế toán BTC trên Hóa đơn, Báo giá và Phiếu thu chi. | ✅ Sẵn sàng |
| **`l10n_vn_cash_voucher`** | **Phiếu Thu (01-TT) & Phiếu Chi (02-TT)**: In phiếu thu và phiếu chi chuẩn Thông tư 200/2014/TT-BTC của Bộ Tài chính với đầy đủ định khoản Nợ/Có và 5 chữ ký pháp lý. | ✅ Sẵn sàng |
| **`l10n_vn_stock_voucher`** | **Phiếu Nhập (01-VT) & Phiếu Xuất (02-VT)**: In phiếu nhập kho và xuất kho chuẩn Thông tư 200/2014/TT-BTC với bảng kê chi tiết vật tư, số lượng thực tế và 5 chữ ký kế toán kho. | ✅ Sẵn sàng |
| **`l10n_vn_vat_declaration`** | **Bảng kê Thuế GTGT (01-1 & 01-2/GTGT)**: Tự động kết xuất bảng kê hóa đơn mua vào và bán ra theo mẫu Tổng cục Thuế, phục vụ đối chiếu và nhập phần mềm HTKK. | ✅ Sẵn sàng |
| **`l10n_vn_payroll_pit`** | **Thuế TNCN & Bảo Hiểm Xã Hội**: Quản lý CCCD, MST cá nhân, mã số BHXH, số người phụ thuộc và công cụ tính thuế TNCN lũy tiến 7 bậc / lương Gross → Net theo Luật Lao Động VN. | ✅ Sẵn sàng |
| **`l10n_vn_edi_misa`** | **Hóa đơn điện tử MISA meInvoice**: Tự động phát hành, ký số và đồng bộ hóa đơn điện tử MISA meInvoice trực tiếp từ Hóa đơn khách hàng Odoo chỉ bằng 1 click. | ✅ Sẵn sàng |
| **`payment_vnpay`** | **Cổng thanh toán VNPAY (v2.1.0)**: Tích hợp thanh toán VNPAY-QR, thẻ ATM nội địa & thẻ quốc tế cho Website/eCommerce với chữ ký HMAC-SHA512 và Webhook IPN tự động. | ✅ Sẵn sàng |

### Cách kích hoạt các module trên trong Odoo:
1. Vào menu **Apps (Ứng dụng)**.
2. Bật chế độ Nhà phát triển (**Developer Mode** trong Cài đặt).
3. Bấm nút **Update Apps List (Cập nhật danh sách ứng dụng)**.
4. Tìm kiếm tên module (`l10n_vn_tax_lookup`, `l10n_vn_vietqr_sale` hoặc `l10n_vn_address`) và bấm **Activate (Cài đặt)**.

---

## 📄 Bản quyền
Odoo được phát hành theo giấy phép LGPLv3 / Odoo Enterprise License. Xem chi tiết tại `LICENSE`.
