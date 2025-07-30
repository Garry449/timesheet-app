@echo off
echo ============================================================
echo 🌐 Setting up UAT Domain for Timesheet System
echo ============================================================
echo.

REM Get the current IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set IP=%%a
    goto :found_ip
)

:found_ip
set IP=%IP: =%

echo 📍 Your IP Address: %IP%
echo 🌐 UAT Domain: uat-timesheet.local
echo.
echo 📝 This will add the following line to your hosts file:
echo    %IP% uat-timesheet.local
echo.

REM Check if entry already exists
findstr "uat-timesheet.local" C:\Windows\System32\drivers\etc\hosts >nul
if %errorlevel% equ 0 (
    echo ✅ UAT domain already configured in hosts file
) else (
    echo 📝 Adding UAT domain to hosts file...
    echo # UAT Timesheet System >> C:\Windows\System32\drivers\etc\hosts
    echo %IP% uat-timesheet.local >> C:\Windows\System32\drivers\etc\hosts
    echo ✅ UAT domain added successfully!
)

echo.
echo 🎉 Setup Complete!
echo.
echo 📱 Access your UAT environment at:
echo    http://uat-timesheet.local:8080
echo.
echo 📋 For other devices on your network:
echo    http://%IP%:8080
echo.
pause 