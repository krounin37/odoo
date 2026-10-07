# Module Odoo: Tích Hợp Đơn Vị Giao Vận Giao Hàng Tiết Kiệm (delivery_ghtk)

Module tích hợp đơn vị vận chuyển hàng đầu tại Việt Nam - **Giao Hàng Tiết Kiệm (GHTK)** với phân hệ Bán hàng (Sales) và Kho vận (Inventory) của Odoo.

### 🌟 Tính năng chính:
- **Tự động tính cước vận chuyển (Shipping Rate Calculation)**:
  - Tự động tính cước vận chuyển dự tính trên Báo giá & Đơn hàng bán dựa trên Địa chỉ người nhận (kết hợp cấp Tỉnh/Huyện của module `l10n_vn_address`) và tổng khối lượng sản phẩm.
  - Phân biệt cước nội tỉnh và liên tỉnh, tự động xử lý khi ở chế độ thử nghiệm (Staging) hoặc thực tế (Production).
- **Đẩy đơn giao vận 1-Click (Submit Shipment Order)**:
  - Trên Phiếu xuất kho (`stock.picking`), chỉ cần xác nhận đơn giao hàng, hệ thống tự động gọi API đẩy đơn sang hệ thống GHTK.
  - Truyền đầy đủ: Thông tin người nhận, số điện thoại, địa chỉ chi tiết, danh sách sản phẩm, tiền thu hộ COD (`ghtk_cod_amount`).
  - Nhận về ngay **Mã vận đơn chính thức (Tracking Number)** từ GHTK.
- **In tem nhãn vận đơn A6 (Print Shipping Label)**:
  - Nút **"In Tem Nhãn GHTK"** trực tiếp trên Header của phiếu giao hàng, mở ngay trang in tem nhãn chuẩn A6/A7 của GHTK để dán lên kiện hàng.
- **Tra cứu hành trình đơn hàng thời gian thực**:
  - Tích hợp link tra cứu vận đơn trực tuyến trên website của GHTK, giúp nhân viên và khách hàng kiểm tra vị trí đơn hàng 24/7.

### 🚀 Hướng dẫn kích hoạt & Cấu hình:
1. Vào menu **Apps (Ứng dụng)** > Bật Developer Mode > Bấm **Update Apps List**.
2. Tìm kiếm `delivery_ghtk` hoặc `GHTK` và bấm **Activate (Cài đặt)**.
3. Vào **Sales (Bán hàng) hoặc Inventory (Kho vận) > Configuration > Shipping Methods (Phương thức giao hàng)**.
4. Mở phương thức **Giao Hàng Tiết Kiệm (GHTK)**:
   - Điền **GHTK API Token** do GHTK cấp.
   - Chọn môi trường: **Thử nghiệm (Staging)** hoặc **Chính thức (Production)**.
   - Cấu hình thông tin kho lấy hàng: Địa chỉ, Quận/Huyện, Tỉnh/Thành phố, Số điện thoại shop.
   - Chọn người trả cước: **Shop trả cước (Freeship)** hoặc **Khách trả cước**.
5. Bấm **Save** và xuất bản để sử dụng trên Đơn bán hàng và Website eCommerce!
