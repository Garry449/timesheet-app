@echo off
echo ============================================================
echo 🚀 Starting Timesheet Management System
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 📦 Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo 🌐 Starting server...
echo 📱 The app will be accessible from other devices on your network
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python run_server.py

pause 