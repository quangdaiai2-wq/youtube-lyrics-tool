@echo off
chcp 65001 >nul
title Mo file cau hinh .env de dien khoa API
cd /d "%~dp0"

if not exist ".env" (
    echo.
    echo   KHONG TIM THAY file .env trong thu muc nay.
    echo   Duong dan dang mo:
    echo   %cd%
    echo.
    pause
    exit /b 1
)

echo ============================================================
echo   DANG MO FILE CAU HINH .env
echo ============================================================
echo.
echo   File nay mo bang Notepad.
echo.
echo   Viec cua Dai:
echo     1. Tim dong:  OPENAI_API_KEY="dan_khoa_nous_cua_dai_vao_day"
echo     2. Xoa doan chu  dan_khoa_nous_cua_dai_vao_day
echo     3. Dan khoa Nous Portal cua Dai vao giua hai dau ngoac kep
echo     4. Bam Ctrl + S de luu
echo     5. Dong Notepad, roi chay lai tool
echo.
echo   Khoa Nous Portal bat dau bang:  sk-nous-
echo.

start "" notepad ".env"
exit /b 0
