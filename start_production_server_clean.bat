@echo off
title Timesheet Management System - Clean URL Server
color 0A

echo.
echo ================================================================
echo    TIMESHEET MANAGEMENT SYSTEM - CLEAN URL SERVER
echo ================================================================
echo.
echo Starting production server with clean URLs (no port number)...
echo.

cd /d "%~dp0"

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as Administrator
) else (
    echo ❌ WARNING: Not running as Administrator
    echo Port 80 requires admin privileges
    echo.
    echo Options:
    echo 1. Right-click and "Run as Administrator"
    echo 2. Use port 8080 instead (edit production_server_clean.py)
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements-local.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting clean URL server...
echo.
python production_server_clean.py

echo.
echo Server stopped.
pause 