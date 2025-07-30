@echo off
echo ============================================================
echo 🔧 DEVELOPMENT SERVER - Timesheet Management System
echo ============================================================
echo.
echo ⚠️  WARNING: This is for development only!
echo    Do not use this in production!
echo.
echo 📝 Features:
echo    - Auto-reload on file changes
echo    - Debug mode enabled
echo    - Detailed error messages
echo    - Network access enabled
echo.
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo 🔧 Starting development server...
echo 📱 The app will be accessible from other devices on your network
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Start the development server
python dev_server.py

pause 