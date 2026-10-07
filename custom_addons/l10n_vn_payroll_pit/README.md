# Module Odoo: Quản Lý Thuế TNCN & Bảo Hiểm Xã Hội Việt Nam (l10n_vn_payroll_pit)

Module hỗ trợ phòng Nhân sự (HR) và Kế toán Tiền lương quản lý thông tin bảo hiểm, người phụ thuộc và tự động tính thuế TNCN / Lương Gross - Net theo Luật Lao Động & Luật Thuế TNCN Việt Nam.

### 🌟 Tính năng chính:
- **Quản lý thông tin định danh & thuế cá nhân**:
  - Số Căn cước công dân / CMND (`vn_citizen_id`).
  - Mã số thuế cá nhân TNCN (`vn_tax_code`).
  - Mã số sổ Bảo hiểm xã hội (`vn_social_insurance_no`).
  - Số người phụ thuộc đăng ký giảm trừ gia cảnh (`vn_dependent_count`).
- **Tự động trích nộp Bảo hiểm bắt buộc**:
  - **Người lao động đóng (10.5%)**: BHXH 8%, BHYT 1.5%, BHTN 1%.
  - **Doanh nghiệp đóng (23.5%)**: BHXH 17.5%, BHYT 3%, BHTN 1%, Kinh phí công đoàn 2%.
- **Tính Thuế TNCN lũy tiến từng phần 7 bậc (Thông tư 111/2013/TT-BTC)**:
  - Mức giảm trừ bản thân: 11.000.000 VNĐ/tháng.
  - Mức giảm trừ người phụ thuộc: 4.400.000 VNĐ/người/tháng.
  - Tự động trừ các khoản bảo hiểm bắt buộc trước khi tính thuế.
  - Áp dụng chuẩn xác 7 bậc thuế: 5%, 10%, 15%, 20%, 25%, 30%, 35%.
- **Công cụ tính Lương Gross → Net tức thì (Gross-to-Net Calculator)**:
  - Nhập mức lương Gross & Mức lương đóng BHXH trên hồ sơ nhân viên (`hr.employee`).
  - Hệ thống tự động tính toán tức thì: Tổng bảo hiểm NLĐ, Tổng bảo hiểm công ty, Thu nhập tính thuế, Tiền thuế TNCN và Lương thực nhận (Net).

### 🚀 Cách kích hoạt trong Odoo:
1. Vào **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm `l10n_vn_payroll_pit` hoặc `Thuế TNCN` và bấm **Activate (Cài đặt)**.
3. Vào phân hệ **Employees (Nhân viên)** > Mở một nhân viên > Xem tab **"Thuế TNCN & Bảo Hiểm VN"**.
