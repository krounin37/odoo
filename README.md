# Odoo Project Setup & Deployment Guide

<p align="center">
  <a href="README.md"><b>English</b></a> |
  <a href="README.vi.md"><b>Tiếng Việt</b></a> |
  <a href="README.zh.md"><b>简体中文</b></a>
</p>

---

## 📌 Overview

This repository contains the source code for the **Odoo** ERP platform along with Docker configurations for quick setup and local development.

---

## 🚀 Quick Start (Docker - Recommended)

The easiest and fastest way to run Odoo and its PostgreSQL database is using **Docker Compose**.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed and running
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)

### 1. Start Services
Run the following command in the project root directory:

```bash
docker compose up -d
```

This starts:
- **web**: Odoo web service exposed on port `8069`
- **db**: PostgreSQL 16 database server

### 2. Access Odoo
Open your browser and navigate to:
```
http://localhost:8069
```

On first access, fill in the database creation form:
- **Master Password**: Keep safe (used to manage/drop databases)
- **Database Name**: e.g., `odoo_db`
- **Email / Password**: Your administrator login credentials
- **Language / Country**: Select according to your needs
- **Demo data**: Check if you want sample data

### 3. Common Docker Commands

- **View web service logs**:
  ```bash
  docker compose logs -f web
  ```
- **Stop containers**:
  ```bash
  docker compose down
  ```
- **Stop containers and remove volumes (reset database)**:
  ```bash
  docker compose down -v
  ```
- **Restart containers**:
  ```bash
  docker compose restart
  ```

---

## 🛠️ Local Python Setup (Bare Metal / Development)

If you prefer to run Odoo directly with Python without Docker:

### Prerequisites
- Python 3.10, 3.11, or 3.12
- PostgreSQL 14+ installed and running
- `wkhtmltopdf` (recommended for generating PDF reports)

### 1. Create and Activate Virtual Environment

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Configure Database User
Create a PostgreSQL user for Odoo:

```bash
createuser -s odoo
createdb -O odoo odoo_db
```

### 4. Create Configuration File (`odoo.conf`)
Create an `odoo.conf` file in the root directory:

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

### 5. Run Odoo Server

```bash
# Using configuration file
python odoo-bin -c odoo.conf

# Or via command line flags
python odoo-bin --addons-path=addons -d odoo_db --db_user=odoo --db_password=odoo
```

---

## 💡 Developer Commands

- **Enable Developer Mode flags (auto-reload python & assets)**:
  ```bash
  python odoo-bin -c odoo.conf --dev=all
  ```
- **Install a module**:
  ```bash
  python odoo-bin -c odoo.conf -d odoo_db -i <module_name>
  ```
- **Upgrade a module**:
  ```bash
  python odoo-bin -c odoo.conf -d odoo_db -u <module_name>
  ```

---

## 🇻🇳 Vietnam Localization Addons (`custom_addons/`)

This repository includes custom modules tailored for Vietnamese business operations:

| Module | Name & Function | Status |
| :--- | :--- | :---: |
| **`l10n_vn_tax_lookup`** | **Tự động tra cứu Mã số thuế**: Tra cứu tức thì tên doanh nghiệp, địa chỉ và trạng thái hoạt động từ dữ liệu Tổng cục Thuế khi nhập MST. | ✅ Sẵn sàng |
| **`l10n_vn_vietqr_sale`** | **VietQR trên Báo giá & Đơn hàng**: Tự động sinh mã VietQR NAPAS 247 kèm số tiền và nội dung đơn hàng trên Form view và file PDF in ra. | ✅ Sẵn sàng |
| **`l10n_vn_address`** | **Địa giới hành chính 3 cấp**: Quản lý Quận/Huyện và Phường/Xã với bộ lọc liên hoàn và nút tự động chuẩn hóa chuỗi địa chỉ giao hàng / xuất hóa đơn. | ✅ Sẵn sàng |

### How to Activate Custom Modules in Odoo:
1. Go to **Apps** (Ứng dụng).
2. Activate **Developer Mode** (Chế độ nhà phát triển trong Settings).
3. Click **Update Apps List** (Cập nhật danh sách ứng dụng).
4. Search for the module name (`l10n_vn_tax_lookup`, `l10n_vn_vietqr_sale`, or `l10n_vn_address`) and click **Activate (Cài đặt)**.

---

## 📄 License
Odoo is published under LGPLv3 / Odoo Enterprise License. See `LICENSE` for details.
