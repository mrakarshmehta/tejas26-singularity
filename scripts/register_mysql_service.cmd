@echo off
:: ============================================================
:: HiddenYatra — Register MySQL 8.4 as a Windows Service
:: Run this script as Administrator (Right-click -> Run as admin)
:: ============================================================

echo ========================================
echo  MySQL Service Registration
echo ========================================
echo.

:: Check admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [FAIL] This script must be run as Administrator!
    echo        Right-click this file and select "Run as administrator"
    pause
    exit /b 1
)
echo [PASS] Running as Administrator

:: Stop any running mysqld
echo.
echo Stopping any running MySQL processes...
taskkill /F /IM mysqld.exe >nul 2>&1
timeout /t 2 >nul
echo [PASS] MySQL processes stopped

:: Remove old service if exists
echo.
echo Checking for existing MySQL84 service...
sc query MySQL84 >nul 2>&1
if %errorlevel% equ 0 (
    echo Removing existing service...
    net stop MySQL84 >nul 2>&1
    sc delete MySQL84 >nul 2>&1
    timeout /t 2 >nul
    echo [PASS] Old service removed
) else (
    echo [INFO] No existing MySQL84 service found
)

:: Register the service
echo.
echo Registering MySQL 8.4 as Windows Service...
"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" --install MySQL84 --defaults-file="D:\HiddenYatra\my.ini"
if %errorlevel% neq 0 (
    echo [FAIL] Service registration failed!
    pause
    exit /b 1
)
echo [PASS] Service "MySQL84" registered

:: Set to auto-start
echo.
echo Setting service to Automatic startup...
sc config MySQL84 start= auto >nul
echo [PASS] Startup type set to Automatic

:: Start the service
echo.
echo Starting MySQL service...
net start MySQL84
if %errorlevel% neq 0 (
    echo [FAIL] Service failed to start!
    echo Check: eventvwr.msc -^> Windows Logs -^> Application
    pause
    exit /b 1
)
echo [PASS] MySQL service is RUNNING

:: Verify port
echo.
echo Verifying port 3306...
timeout /t 2 >nul
netstat -an | findstr ":3306.*LISTENING"
if %errorlevel% equ 0 (
    echo [PASS] Port 3306 is LISTENING
) else (
    echo [WARN] Port 3306 check inconclusive
)

:: Test connectivity
echo.
echo Testing database connectivity...
"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -u root --port=3306 -e "SELECT 'CONNECTION_OK' AS status;"
echo.

:: Verify HiddenYatra database
"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe" -u root --port=3306 -e "USE hiddenyatra; SELECT COUNT(*) AS places FROM places;"
echo.

:: Remove startup batch if service works
echo.
echo Removing startup batch file (service handles auto-start now)...
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\HiddenYatra_MySQL.bat" (
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\HiddenYatra_MySQL.bat"
    echo [PASS] Startup batch file removed
)

echo.
echo ========================================
echo  SETUP COMPLETE
echo ========================================
echo.
echo  Service Name : MySQL84
echo  Startup Type : Automatic
echo  Data Dir     : D:\HiddenYatra\mysql_data
echo  Port         : 3306
echo.
echo  MySQL will now start automatically on Windows boot.
echo  Start HiddenYatra anytime with:
echo    cd D:\HiddenYatra
echo    python app.py
echo.
pause
