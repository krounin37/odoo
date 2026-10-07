# Module Odoo: Bảng Kê Thuế GTGT Mua Vào (01-2/GTGT) & Bán Ra (01-1/GTGT) (l10n_vn_vat_declaration)

Module hỗ trợ phòng kế toán doanh nghiệp Việt Nam tự động kết xuất bảng kê hóa đơn mua vào và bán ra phục vụ đối chiếu thuế GTGT và nhập liệu phần mềm HTKK của Tổng cục Thuế.

### 🌟 Tính năng chính:
- **Bảng kê bán ra (Mẫu 01-1/GTGT)**:
  - Tự động gom toàn bộ hóa đơn bán ra (`out_invoice`) và hóa đơn điều chỉnh giảm (`out_refund`) trong kỳ chọn.
  - Hiển thị đầy đủ: Số HĐ/Ký hiệu, Ngày HĐ, Tên khách hàng, Mã số thuế khách hàng, Doanh thu chưa thuế, Tiền thuế GTGT.
  - Tổng cộng doanh thu và tiền thuế bán ra.
- **Bảng kê mua vào (Mẫu 01-2/GTGT)**:
  - Tự động gom toàn bộ hóa đơn mua vào (`in_invoice`) và điều chỉnh giảm (`in_refund`) trong kỳ chọn.
  - Hiển thị đầy đủ: Số HĐ, Ngày HĐ, Tên nhà cung cấp, Mã số thuế NCC, Doanh số mua chưa thuế, Tiền thuế GTGT đầu vào được khấu trừ.
  - Tổng cộng giá trị mua và tiền thuế khấu trừ.
- **Tính năng tra cứu nhanh trên màn hình**:
  - Nút **"Xem Hóa Đơn Trên Màn Hình"**: Lọc danh sách hóa đơn tức thì để đối chiếu trước khi xuất báo cáo.
  - Nút **"Xuất PDF Bảng Kê"**: Kết xuất file PDF bảng kê đẹp mắt chuẩn mẫu Tổng cục Thuế kèm đầy đủ chữ ký 3 bên (Người lập biểu, Kế toán trưởng, Người đại diện pháp luật).

### 🚀 Cách sử dụng:
1. Vào **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm `l10n_vn_vat_declaration` hoặc `Bảng Kê Thuế` và bấm **Activate (Cài đặt)**.
3. Vào phân hệ **Accounting (Kế toán) > Reporting (Báo cáo) > Bảng Kê Thuế GTGT (01-1 & 01-2)**.
4. Chọn khoảng thời gian (Từ ngày - Đến ngày), Loại bảng kê (Mua vào, Bán ra hoặc Cả hai), sau đó bấm **Xuất PDF** hoặc **Xem trên màn hình**.
