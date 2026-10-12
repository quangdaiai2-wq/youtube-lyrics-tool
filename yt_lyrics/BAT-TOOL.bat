@echo off
chcp 65001 >nul
title Tool trich xuat loi bai hat YouTube
cd /d "%~dp0"

echo ============================================================
echo   TOOL TRICH XUAT LOI BAI HAT YOUTUBE
echo ============================================================
echo.
echo   Day la ban chay CO CUA SO - dung khi can xem thong bao loi.
echo   (Ban chay an, khong hien cua so: nhan dup file CHAY-TOOL.vbs
echo    o thu muc goc du an.)
echo.
echo   Dang bat tool, trinh duyet se tu mo sau vai giay...
echo.

set WHISPER_MODEL=base

"C:\Users\nguye\.workbuddy-ai\binaries\python\envs\default\Scripts\python.exe" app.py

echo.
echo   Tool da dung. Nhan phim bat ky de dong cua so nay.
pause >nul
