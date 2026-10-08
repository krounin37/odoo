@echo off
setlocal enabledelayedexpansion

if "%~1"=="" (
    echo [WARNING] Vui long keo tha file .dump vao day hoac truyen duong dan file!
    echo Cach dung: scripts\restore_db.bat .\backups\techzone_xxxx.dump [target_db]
    pause
    exit /b 1
)

set BACKUP_FILE=%~1
set TARGET_DB=%~2
if "%TARGET_DB%"=="" set TARGET_DB=techzone

echo [INFO] Dang phuc hoi co so du lieu '%TARGET_DB%' tu %BACKUP_FILE%...
docker exec odoo-db-1 psql -U odoo -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '%TARGET_DB%' AND pid <> pg_backend_pid();" > nul 2>&1
docker exec odoo-db-1 dropdb -U odoo --if-exists "%TARGET_DB%"
docker exec odoo-db-1 createdb -U odoo "%TARGET_DB%"

docker exec -i odoo-db-1 pg_restore -U odoo -d "%TARGET_DB%" < "%BACKUP_FILE%"

echo [SUCCESS] Phuc hoi hoan tat co so du lieu '%TARGET_DB%'!
pause
