@echo off
setlocal enabledelayedexpansion

:: Lay timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%

set BACKUP_DIR=.\backups
set BACKUP_FILE=%BACKUP_DIR%\techzone_%TIMESTAMP%.dump

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo [INFO] Dang tien hanh sao luu co so du lieu 'techzone'...
docker exec odoo-db-1 pg_dump -U odoo -Fc -d techzone > "%BACKUP_FILE%"

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Sao luu thanh cong: %BACKUP_FILE%
) else (
    echo [ERROR] Sao luu that bai!
)
pause
