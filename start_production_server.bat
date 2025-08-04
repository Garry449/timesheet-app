@echo off
title Timesheet Management System - Production Server
color 0A

echo.
echo ================================================================
echo    TIMESHEET MANAGEMENT SYSTEM - PRODUCTION SERVER
echo ================================================================
echo.
echo Starting production server for multi-user access...
echo.

cd /d "%~dp0"

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
echo Starting server...
echo.
python production_server.py

echo.
echo Server stopped.
pause 