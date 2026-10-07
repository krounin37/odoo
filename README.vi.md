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

## 📄 Bản quyền
Odoo được phát hành theo giấy phép LGPLv3 / Odoo Enterprise License. Xem chi tiết tại `LICENSE`.
