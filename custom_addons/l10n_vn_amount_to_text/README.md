# Module Odoo: Đọc Số Tiền Thành Chữ Tiếng Việt (l10n_vn_amount_to_text)

Module tuân thủ Luật Kế toán Việt Nam và quy định BTC về thể hiện số tiền bằng chữ trên chứng từ tài chính.

### 🌟 Tính năng chính:
- **Thuật toán đọc số chuẩn xác**:
  - Hỗ trợ đầy đủ các quy tắc phát âm và ngữ pháp: "mười một", "hai mươi mốt", "mười lăm", "lăm mươi lăm", "linh / lẻ", hàng trăm tỷ, triệu tỷ,...
  - Hậu tố đơn vị tiền tệ chuẩn: "đồng chẵn", "đô la Mỹ", "euro",...
- **Tích hợp đồng bộ trên các phân hệ**:
  - **Hóa đơn (`account.move`)**: Trường `amount_total_words_vn` tự động tính theo tổng tiền hóa đơn.
  - **Phiếu thanh toán (`account.payment`)**: Trường `amount_words_vn` phục vụ phiếu thu, phiếu chi.
  - **Báo giá & Đơn bán hàng (`sale.order`)**: Trường `amount_total_words_vn`.
- **Mẫu in PDF**:
  - Kế thừa hóa đơn PDF (`account.report_invoice_document`) tự động bổ sung dòng *"Số tiền bằng chữ: ... đồng chẵn."* phía dưới tổng tiền.

### 🚀 Cách kích hoạt trong Odoo:
1. Vào **Apps (Ứng dụng)**.
2. Bật **Developer Mode** (Chế độ nhà phát triển).
3. Bấm **Update Apps List**.
4. Tìm kiếm `l10n_vn_amount_to_text` hoặc `Đọc Số Tiền` và bấm **Activate (Cài đặt)**.
