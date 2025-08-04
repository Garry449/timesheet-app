@echo off
title Setup Custom Domain for Timesheet System
color 0B

echo.
echo ================================================================
echo    SETTING UP CUSTOM DOMAIN FOR TIMESHEET SYSTEM
echo ================================================================
echo.

REM Get current IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    goto :found_ip
)
:found_ip
set IP=%IP: =%

echo Current IP Address: %IP%
echo.

echo Choose your custom domain name:
echo 1. timesheet.local
echo 2. company-timesheet.local  
echo 3. timesheet.company.local
echo 4. Custom (enter your own)
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" set DOMAIN=timesheet.local
if "%choice%"=="2" set DOMAIN=company-timesheet.local
if "%choice%"=="3" set DOMAIN=timesheet.company.local
if "%choice%"=="4" (
    set /p DOMAIN="Enter your custom domain: "
)

echo.
echo Setting up domain: %DOMAIN%
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as Administrator
) else (
    echo ❌ This script requires Administrator privileges
    echo Please right-click and "Run as Administrator"
    pause
    exit /b 1
)

REM Backup hosts file
echo Creating backup of hosts file...
copy "C:\Windows\System32\drivers\etc\hosts" "C:\Windows\System32\drivers\etc\hosts.backup" >nul 2>&1

REM Add entry to hosts file
echo Adding %IP% %DOMAIN% to hosts file...
echo %IP% %DOMAIN% >> "C:\Windows\System32\drivers\etc\hosts"

echo.
echo ================================================================
echo    CUSTOM DOMAIN SETUP COMPLETE!
echo ================================================================
echo.
echo ✅ Domain configured: %DOMAIN%
echo ✅ IP Address: %IP%
echo.
echo 🌐 Users can now access your timesheet system at:
echo    http://%DOMAIN%
echo.
echo 📝 Next steps:
echo    1. Start your server with: start_production_server_clean.bat
echo    2. Share http://%DOMAIN% with your users
echo    3. Test the connection
echo.
echo 🔧 To remove this domain later, edit:
echo    C:\Windows\System32\drivers\etc\hosts
echo.
pause 