#!/bin/bash
# Script phục hồi cơ sở dữ liệu Odoo TechZone từ file dump
if [ -z "$1" ]; then
    echo "⚠️ Vui lòng chỉ định đường dẫn file backup để phục hồi!"
    echo "Cách dùng: bash scripts/restore_db.sh ./backups/techzone_YYYYMMDD_HHMMSS.dump [target_db_name]"
    exit 1
fi

BACKUP_FILE="$1"
TARGET_DB="${2:-techzone}"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Không tìm thấy file backup: $BACKUP_FILE"
    exit 1
fi

echo "⏳ Đang phục hồi cơ sở dữ liệu '$TARGET_DB' từ $BACKUP_FILE..."
# Ngắt kết nối cũ và tạo lại database nếu cần
docker exec odoo-db-1 psql -U odoo -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$TARGET_DB' AND pid <> pg_backend_pid();" > /dev/null 2>&1
docker exec odoo-db-1 dropdb -U odoo --if-exists "$TARGET_DB"
docker exec odoo-db-1 createdb -U odoo "$TARGET_DB"

# Phục hồi dữ liệu
docker exec -i odoo-db-1 pg_restore -U odoo -d "$TARGET_DB" < "$BACKUP_FILE"

echo "✅ Phục hồi hoàn tất cho cơ sở dữ liệu '$TARGET_DB'!"
