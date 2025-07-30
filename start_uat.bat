@echo off
echo ============================================================
echo 🌐 UAT Timesheet Management System
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
echo 🌐 Setting up UAT domain...
call setup_uat_domain.bat

echo.
echo 🚀 Starting UAT server...
echo 📱 Access at: http://uat-timesheet.local:8080
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Start the UAT server
python uat_server.py

pause 