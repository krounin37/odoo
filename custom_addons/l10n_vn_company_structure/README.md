# Module Odoo: Cơ Cấu Tổ Chức Phòng Ban & Quy Trình Doanh Nghiệp Chuẩn (l10n_vn_company_structure)

Module thiết lập sẵn sơ đồ cây 15 phòng ban, 32 vị trí chức danh công việc và chuẩn hóa quy trình vận hành liên phòng ban cho doanh nghiệp hoạt động trên nền tảng Odoo.

---

## 🏛️ Sơ Đồ Cơ Cấu Tổ Chức Phòng Ban (15 Phòng Ban & 32 Chức Danh)

```text
CÔNG TY CỔ PHẦN CÔNG NGHỆ TECHZONE
│
├── 1. Ban Giám Đốc (Board of Directors)
│   ├── Tổng Giám Đốc (CEO)
│   └── Phó Tổng Giám Đốc / COO
│
├── 2. Khối Kinh Doanh & Tiếp Thị (Commercial Division)
│   ├── Giám Đốc Kinh Doanh (CCO)
│   ├── 2.1. Phòng Kinh Doanh (Sales)
│   │   ├── Trưởng Phòng Kinh Doanh
│   │   ├── Chuyên Viên Kinh Doanh B2B
│   │   └── Nhân Viên Bán Lẻ / Showroom
│   ├── 2.2. Phòng Marketing
│   │   ├── Trưởng Phòng Marketing
│   │   ├── Chuyên Viên Digital Marketing
│   │   └── Nhân Viên Sáng Tạo Nội Dung (Content)
│   └── 2.3. Phòng Chăm Sóc Khách Hàng (Customer Service)
│       ├── Trưởng Nhóm CSKH
│       └── Chuyên Viên Hỗ Trợ & CSKH
│
├── 3. Khối Tài Chính - Kế Toán (Finance & Accounting)
│   ├── Giám Đốc Tài Chính (CFO)
│   └── 3.1. Phòng Kế Toán
│       ├── Kế Toán Trưởng
│       ├── Kế Toán Bán Hàng & Công Nợ Phải Thu (AR)
│       ├── Kế Toán Mua Hàng & Công Nợ Phải Trả (AP)
│       ├── Kế Toán Thuế & Ngân Hàng
│       └── Kế Toán Kho & Giá Thành
│
├── 4. Khối Vận Hành & Chuỗi Cung Ứng (Operations & Supply Chain)
│   ├── Giám Đốc Vận Hành (Operations Manager)
│   ├── 4.1. Phòng Mua Hàng (Purchasing / Procurement)
│   │   ├── Trưởng Phòng Mua Hàng
│   │   └── Chuyên Viên Mua Hàng
│   └── 4.2. Phòng Quản Lý Kho & Giao Vận (Inventory & Logistics)
│       ├── Thủ Kho Trưởng
│       ├── Nhân Viên Kho Vận
│       └── Nhân Viên Điều Phối Đơn Hàng (Dispatcher)
│
├── 5. Khối Hành Chính - Nhân Sự (HR & Administration)
│   ├── Trưởng Khối Hành Chính - Nhân Sự
│   ├── 5.1. Phòng Nhân Sự (HR)
│   │   ├── Trưởng Phòng Nhân Sự
│   │   ├── Chuyên Viên Tuyển Dụng & Đào Tạo
│   │   └── Chuyên Viên C&B (Tiền Lương & Bảo Hiểm)
│   └── 5.2. Phòng Hành Chính & Quản Trị
│       ├── Chuyên Viên Hành Chính - Văn Phòng
│       └── Nhân Viên Lễ Tân & Pháp Chế
│
└── 6. Phòng Công Nghệ Thông Tin (IT & Systems)
    ├── Trưởng Phòng IT
    ├── Chuyên Viên Quản Trị Hệ Thống Odoo
    └── Kỹ Sư Hạ Tầng & Bảo Mật
```

---

## 🔄 5 Quy Trình Vận Hành Doanh Nghiệp Chuẩn Trên Odoo

### Quy trình 1: Bán Hàng & Thu Tiền (Order-to-Cash — O2C)
1. **Marketing & CRM**: Phòng Marketing thu thập khách hàng tiềm năng qua Website/Chiến dịch -> Chuyển thành Cơ hội trong CRM.
2. **Kinh doanh (Sales)**: Nhân viên Sales liên hệ, tạo Báo giá (Quotation), kiểm tra tồn kho -> Tự động sinh mã **VietQR động** (`l10n_vn_vietqr_sale`) gửi khách hàng -> Khách xác nhận -> Chuyển thành Đơn bán hàng (Sale Order).
3. **Kho vận (Logistics)**: Hệ thống tự động sinh Phiếu xuất kho (Delivery Order) -> Thủ kho soạn hàng, đóng gói, in Phiếu xuất kho mẫu 02-VT (`l10n_vn_stock_voucher`) -> Bấm 1-click đẩy đơn giao vận sang **GHTK** (`delivery_ghtk`) lấy mã vận đơn và in tem nhãn dán kiện hàng.
4. **Kế toán (Accounting)**: Khi đơn hàng giao thành công -> Kế toán lập Hóa đơn bán ra -> Đọc số tiền bằng chữ Tiếng Việt (`l10n_vn_amount_to_text`) -> Bấm 1-click phát hành Hóa đơn điện tử **MISA meInvoice** (`l10n_vn_edi_misa`) -> Ghi nhận thanh toán (qua VNPAY / VietQR) -> In Phiếu Thu mẫu 01-TT (`l10n_vn_cash_voucher`).

### Quy trình 2: Mua Hàng & Thanh Toán (Procure-to-Pay — P2P)
1. **Dự báo nhu cầu**: Khi tồn kho giảm xuống dưới mức an toàn hoặc có đơn bán hàng -> Odoo tự động sinh Yêu cầu báo giá mua hàng (RFQ).
2. **Mua hàng (Purchasing)**: Chuyên viên mua hàng liên hệ nhà cung cấp, đàm phán giá -> Trưởng phòng duyệt -> Xác nhận Đơn mua hàng (PO).
3. **Kho vận (Warehouse)**: Thủ kho kiểm đếm hàng thực nhận -> Xác nhận Phiếu nhập kho và in Phiếu Nhập Kho mẫu 01-VT chuẩn Bộ Tài chính (`l10n_vn_stock_voucher`).
4. **Kế toán (Accounting)**: Nhận hóa đơn mua vào từ nhà cung cấp -> Đối soát 3 bên (PO - Phiếu Nhập - Hóa đơn) -> Đưa vào Bảng kê thuế GTGT mua vào 01-2/GTGT (`l10n_vn_vat_declaration`) -> Khi thanh toán chi tiền: Lập Phiếu Chi mẫu 02-TT (`l10n_vn_cash_voucher`).

### Quy trình 3: Quản Lý Kho & Kiểm Kê (Inventory Management)
1. **Thiết lập định mức**: Cài đặt mức tồn kho tối thiểu / tối đa cho từng mặt hàng (Reordering Rules).
2. **Theo dõi vị trí kho**: Quản lý nhiều kho hàng, phân khu vực (Kệ, Tầng, Dãy).
3. **Kiểm kê định kỳ**: Thực hiện kiểm kê định kỳ tháng/quý -> Odoo tự động tính số lượng chênh lệch (thừa/thiếu) và sinh bút toán điều chỉnh kho.

### Quy trình 4: Kế Toán & Kê Khai Thuế Định Kỳ (Financial Accounting & Tax)
1. **Sổ quỹ & Ngân hàng**: Đối soát sao kê ngân hàng hàng ngày, quản lý các khoản thu chi.
2. **Báo cáo Thuế hàng tháng / hàng quý**: Vào phân hệ Kế toán -> Mở Bảng Kê Thuế GTGT (`l10n_vn_vat_declaration`) -> Xuất bảng kê hóa đơn bán ra (01-1) và mua vào (01-2) để nộp thuế hoặc nhập vào phần mềm HTKK của Tổng cục Thuế.

### Quy trình 5: Nhân Sự, Chấm Công & Tiền Lương (HR & Payroll)
1. **Hồ sơ nhân sự**: Quản lý thông tin định danh: CCCD, MST cá nhân, mã số sổ BHXH, số người phụ thuộc (`l10n_vn_payroll_pit`).
2. **Phòng ban & Vị trí**: Gắn nhân viên vào đúng Phòng ban và Chức danh công việc đã thiết lập.
3. **Tính lương cuối tháng**:
   - Tự động trích đóng Bảo hiểm bắt buộc: NLĐ đóng 10.5%, Doanh nghiệp đóng 23.5%.
   - Tự động tính Giảm trừ gia cảnh bản thân (11 triệu) & người phụ thuộc (4.4 triệu/người).
   - Tự động tính Thuế TNCN lũy tiến 7 bậc (Thông tư 111/2013/TT-BTC) và chuyển đổi Lương Gross -> Lương Net.
   - Kế toán duyệt chi lương và hạch toán chi phí nhân công.
