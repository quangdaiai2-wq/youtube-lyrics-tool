@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "yt_lyrics\app.py" (
    echo.
    echo   KHONG TIM THAY thu muc yt_lyrics.
    echo   Duong dan dang mo:
    echo   %cd%
    echo.
    pause
    exit /b 1
)

rem Chay tool o che do AN - khong hien cua so den.
rem Toan bo phan chay nam trong CHAY-TOOL.vbs.
wscript.exe //nologo "%~dp0CHAY-TOOL.vbs"
exit /b 0
