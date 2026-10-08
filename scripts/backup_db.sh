#!/bin/bash
# Script sao lưu tự động cơ sở dữ liệu Odoo TechZone
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"
BACKUP_FILE="${BACKUP_DIR}/techzone_${TIMESTAMP}.dump"

mkdir -p "$BACKUP_DIR"

echo "⏳ Đang tiến hành sao lưu cơ sở dữ liệu 'techzone'..."
docker exec odoo-db-1 pg_dump -U odoo -Fc -d techzone > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✅ Sao lưu thành công: $BACKUP_FILE (Dung lượng: $FILE_SIZE)"
else
    echo "❌ Sao lưu thất bại!"
    exit 1
fi
