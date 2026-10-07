# Custom Addons Directory

Thư mục này dùng để chứa các module tùy biến (custom modules) hoặc các module bên thứ ba (như module bản địa hóa Việt Nam, cổng thanh toán, hóa đơn điện tử, vận chuyển,...).

### Cấu trúc khuyến nghị:
```text
custom_addons/
├── l10n_vn_address/        # Ví dụ: Module địa giới hành chính VN
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   └── views/
└── your_custom_module/
```

### Lưu ý khi sử dụng:
1. Mỗi thư mục con trong đây phải là một Odoo module hợp lệ (có file `__manifest__.py` và `__init__.py`).
2. Nếu clone từ Git bên ngoài về thư mục này, nhớ xóa thư mục `.git` bên trong module con đó để Git dự án chính theo dõi và lưu code đầy đủ.
3. Trong Docker Compose, thư mục này đã được mount tự động vào `/mnt/extra-addons` của container Odoo.
