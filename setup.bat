@echo off
setlocal enabledelayedexpansion

echo =====================================================================
echo    KHOI TAO HE THONG ODOO ERP TECHZONE (BAN QUYEN & VIET HOA 100%%)
echo =====================================================================
echo.

:: 1. Kiem tra Docker
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] May tinh cua ban chua cai dat Docker hoac Docker Desktop chua chay!
    echo Vui long tai va bat Docker Desktop: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo [1/3] Khoi dong cac container Docker (Odoo Web + PostgreSQL 16)...
docker compose up -d

echo [2/3] Doi PostgreSQL san sang hoat dong...
:WAIT_DB
docker exec odoo-db-1 pg_isready -U odoo >nul 2>nul
if %ERRORLEVEL% neq 0 (
    timeout /t 2 /nobreak >nul
    goto WAIT_DB
)

echo [3/3] Kiem tra va nap co so du lieu tieu chuan (techzone)...
docker exec odoo-db-1 psql -U odoo -lqt | findstr /C:"techzone" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] Phat hien moi truong moi! Dang tu dong phuc hoi database 'techzone' tu file seed...
    docker exec odoo-db-1 createdb -U odoo techzone
    if exist "backups\seed_techzone.dump" (
        docker exec -i odoo-db-1 pg_restore -U odoo -d techzone < backups\seed_techzone.dump
        echo [SUCCESS] Da nap thanh cong co so du lieu 'techzone' day du 12 module va phan quyen!
    ) else (
        echo [WARNING] Khong tim thay backups\seed_techzone.dump. He thong se khoi dong trang.
    )
) else (
    echo [INFO] Co so du lieu 'techzone' da ton tai san tren may. Bo qua buoc nap seed.
)

:: Khoi dong lai web de nhan dien cau hinh moi
docker compose restart web >nul 2>nul

echo.
echo =====================================================================
echo    HE THONG DA SAN SANG SU DUNG!
echo =====================================================================
echo  - Duong link dang nhap: http://localhost:8069/web/login
echo  - Tai khoan Admin      : admin@techzone.vn
echo  - Chuyen vien mua hang : an.nguyen@techzone.vn (Mat khau: Nam@2026)
echo  - Truong phong kinh doanh: sales@techzone.vn (Mat khau: Techzone@2026)
echo  - Ke toan truong       : accountant@techzone.vn (Mat khau: Techzone@2026)
echo  - Thu kho truong       : warehouse@techzone.vn (Mat khau: Techzone@2026)
echo =====================================================================
echo.
pause
