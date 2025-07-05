@echo off
echo.
echo ==========================================
echo    MUSIC PRODUCTION BOT - QUICK START
echo ==========================================
echo.

cd /d "%~dp0"

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from python.org
    pause
    exit /b 1
)

echo.
kecho Booting bot with instant launch...
python boot_bot.py

echo.
echo Bot boot sequence finished!
pause
