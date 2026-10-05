@echo off
chcp 65001 >nul
title Tool trich xuat loi bai hat YouTube
cd /d "%~dp0"

echo ============================================================
echo   TOOL TRICH XUAT LOI BAI HAT YOUTUBE
echo ============================================================
echo.
echo   Dang bat tool, cho vai giay...
echo.

set WHISPER_MODEL=base
start "" http://127.0.0.1:5000

"C:\Users\nguye\.workbuddy-ai\binaries\python\envs\default\Scripts\python.exe" app.py

echo.
echo   Tool da dung. Nhan phim bat ky de dong cua so nay.
pause >nul
