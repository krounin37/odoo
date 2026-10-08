#!/usr/bin/env bash
# Script khởi tạo 1-click hệ thống Odoo ERP TechZone trên Linux / macOS

set -e

echo "====================================================================="
echo "   KHỞI TẠO HỆ THỐNG ODOO ERP TECHZONE (BẢN ĐỊA HÓA VIỆT NAM)"
echo "====================================================================="
echo ""

# 1. Kiểm tra Docker
if ! command -v docker &> /dev/null; then
    echo "❌ [ERROR] Máy tính chưa cài đặt Docker hoặc Docker chưa được bật!"
    exit 1
fi

echo "⏳ [1/3] Khởi động các dịch vụ Docker (Odoo Web + PostgreSQL 16)..."
docker compose up -d

echo "⏳ [2/3] Chờ cơ sở dữ liệu PostgreSQL sẵn sàng..."
until docker exec odoo-db-1 pg_isready -U odoo &> /dev/null; do
    sleep 2
done

echo "⏳ [3/3] Kiểm tra và nạp cơ sở dữ liệu tiêu chuẩn (techzone)..."
if ! docker exec odoo-db-1 psql -U odoo -lqt | cut -d \| -f 1 | grep -qw techzone; then
    echo "💡 [INFO] Phát hiện môi trường mới! Đang tự động phục hồi database 'techzone' từ file seed..."
    docker exec odoo-db-1 createdb -U odoo techzone
    if [ -f "backups/seed_techzone.dump" ]; then
        docker exec -i odoo-db-1 pg_restore -U odoo -d techzone < backups/seed_techzone.dump
        echo "✅ [SUCCESS] Đã nạp thành công database 'techzone' đầy đủ 12 module và phân quyền!"
    else
        echo "⚠️ [WARNING] Không tìm thấy backups/seed_techzone.dump"
    fi
else
    echo "💡 [INFO] Database 'techzone' đã tồn tại sẵn. Bỏ qua bước nạp seed."
fi

# Khởi động lại container web
docker compose restart web > /dev/null 2>&1

echo ""
echo "====================================================================="
echo "   HỆ THỐNG ĐÃ SẴN SÀNG SỬ DỤNG!"
echo "====================================================================="
echo " - Đường link đăng nhập: http://localhost:8069/web/login"
echo " - Tài khoản Admin      : admin@techzone.vn"
echo " - Chuyên viên mua hàng : an.nguyen@techzone.vn (Mật khẩu: Nam@2026)"
echo " - Trưởng phòng kinh doanh: sales@techzone.vn (Mật khẩu: Techzone@2026)"
echo " - Kế toán trưởng       : accountant@techzone.vn (Mật khẩu: Techzone@2026)"
echo " - Thủ kho trưởng       : warehouse@techzone.vn (Mật khẩu: Techzone@2026)"
echo "====================================================================="
echo ""
