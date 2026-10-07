# Module Odoo: Phiếu Nhập Kho (Mẫu 01-VT) & Phiếu Xuất Kho (Mẫu 02-VT) (l10n_vn_stock_voucher)

Module đáp ứng quy định bắt buộc theo Luật Kế toán Việt Nam và Thông tư 200/2014/TT-BTC về quản lý chứng từ vật tư, hàng hóa và kho vận.

### 🌟 Tính năng chính:
- **In Phiếu Nhập Kho (Mẫu số 01 - VT)**: Cho các nghiệp vụ nhập kho hàng hóa, nguyên vật liệu (Receipts/Incoming).
- **In Phiếu Xuất Kho (Mẫu số 02 - VT)**: Cho các nghiệp vụ xuất kho bán hàng, điều chuyển, sản xuất (Delivery/Outgoing).
- **Đầy đủ tiêu chuẩn chứng từ kế toán Việt Nam**:
  - Thông tin công ty (Tên đơn vị, bộ phận, địa chỉ, mã số thuế).
  - Định khoản kế toán: Số phiếu, Nợ TK, Có TK (ví dụ: Nợ 156 / Có 331, Nợ 632 / Có 156).
  - Thông tin người giao / người nhận, lý do nhập/xuất kho.
  - Bảng chi tiết vật tư: Tên hàng, mã số, ĐVT, số lượng chứng từ, số lượng thực nhập/xuất, đơn giá, thành tiền.
  - Tổng số tiền bằng chữ (tích hợp chuẩn ngữ pháp `l10n_vn_amount_to_text`).
  - Số lượng chứng từ gốc đính kèm.
  - Đầy đủ 5 vị trí chữ ký chuẩn Bộ Tài Chính: **Người lập phiếu, Người giao/nhận hàng, Thủ kho, Kế toán trưởng, Thủ trưởng đơn vị (Giám đốc)**.

### 🚀 Cách sử dụng:
1. Vào **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm `l10n_vn_stock_voucher` hoặc `Phiếu Kho` và bấm **Activate (Cài đặt)**.
3. Vào phân hệ **Inventory (Kho vận) > Operations > Transfers (Phiếu giao/nhận kho)**.
4. Chọn một phiếu kho đã hoàn thành (hoặc đang xử lý), bấm nút **Print (In)**:
   - Chọn **In Phiếu Nhập Kho (Mẫu 01 - VT)** (nếu là phiếu nhập)
   - Hoặc chọn **In Phiếu Xuất Kho (Mẫu 02 - VT)** (nếu là phiếu xuất)
   - Hệ thống sẽ kết xuất ngay file PDF chứng từ vật tư chuẩn Bộ Tài chính.
