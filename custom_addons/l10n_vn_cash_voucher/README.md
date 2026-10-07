# Module Odoo: In Phiếu Thu (Mẫu 01-TT) & Phiếu Chi (Mẫu 02-TT) (l10n_vn_cash_voucher)

Module đáp ứng bắt buộc theo quy định Luật Kế toán Việt Nam và Thông tư 200/2014/TT-BTC về mẫu chứng từ kế toán tiền mặt và chuyển khoản.

### 🌟 Tính năng chính:
- **In Phiếu Thu (Mẫu số 01 - TT)**: Dành cho các khoản thu tiền vào (Inbound payment).
- **In Phiếu Chi (Mẫu số 02 - TT)**: Dành cho các khoản chi tiền ra (Outbound payment).
- **Đầy đủ trường pháp lý & nghiệp vụ**:
  - Thông tin doanh nghiệp (Tên đơn vị, địa chỉ, mã số thuế).
  - Định khoản tự động: Số chứng từ, Nợ TK, Có TK.
  - Thông tin người nộp / nhận tiền, địa chỉ, lý do thu/chi.
  - Số tiền bằng số và số tiền viết bằng chữ Tiếng Việt chuẩn (kết hợp `l10n_vn_amount_to_text`).
  - Số lượng chứng từ gốc đính kèm.
  - 5 chữ ký đầy đủ theo mẫu chuẩn Bộ Tài Chính: **Giám đốc, Kế toán trưởng, Người nộp/nhận tiền, Người lập phiếu, Thủ quỹ**.
  - Dòng ký nhận thực tế đã nhận đủ tiền.

### 🚀 Cách sử dụng:
1. Vào menu **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm `l10n_vn_cash_voucher` hoặc `Phiếu Thu Chi` và bấm **Activate (Cài đặt)**.
3. Vào phân hệ **Accounting / Invoicing > Customers > Payments (Thanh toán)** hoặc **Vendors > Payments**.
4. Chọn một thanh toán đã xác nhận, bấm nút **Print (In)**:
   - Chọn **In Phiếu Thu (Mẫu 01 - TT)**
   - Hoặc chọn **In Phiếu Chi (Mẫu 02 - TT)**
   - Hệ thống sẽ tải về ngay file PDF chứng từ chuẩn Bộ Tài chính.
