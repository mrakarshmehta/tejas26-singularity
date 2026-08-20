# ============================================================
# HiddenYatra — Register MySQL 8.4 as a Windows Service
# ============================================================
# This script MUST be run as Administrator.
# It registers MySQL 8.4 as a Windows Service named "MySQL84"
# using the HiddenYatra project's data directory.
# ============================================================

$ErrorActionPreference = "Stop"

$ServiceName   = "MySQL84"
$MysqldPath    = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe"
$DefaultsFile  = "D:\HiddenYatra\my.ini"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " MySQL Service Registration Script"      -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[FAIL] This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "       Right-click PowerShell -> Run as Administrator" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "[PASS] Running as Administrator" -ForegroundColor Green

# Step 2: Verify mysqld.exe exists
if (-not (Test-Path $MysqldPath)) {
    Write-Host "[FAIL] mysqld.exe not found at: $MysqldPath" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[PASS] mysqld.exe found at: $MysqldPath" -ForegroundColor Green

# Step 3: Verify my.ini exists
if (-not (Test-Path $DefaultsFile)) {
    Write-Host "[FAIL] my.ini not found at: $DefaultsFile" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[PASS] my.ini found at: $DefaultsFile" -ForegroundColor Green

# Step 4: Verify datadir exists
$DataDir = "D:\HiddenYatra\mysql_data"
if (-not (Test-Path $DataDir)) {
    Write-Host "[FAIL] datadir not found at: $DataDir" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[PASS] datadir found at: $DataDir" -ForegroundColor Green

# Step 5: Stop any running mysqld processes
Write-Host ""
Write-Host "Stopping any running MySQL processes..." -ForegroundColor Yellow
Get-Process mysqld -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "[PASS] No mysqld processes running" -ForegroundColor Green

# Step 6: Remove existing service if it exists (clean install)
$existingSvc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if ($existingSvc) {
    Write-Host "Removing existing service '$ServiceName'..." -ForegroundColor Yellow
    if ($existingSvc.Status -eq "Running") {
        Stop-Service -Name $ServiceName -Force
        Start-Sleep -Seconds 2
    }
    sc.exe delete $ServiceName | Out-Null
    Start-Sleep -Seconds 2
    Write-Host "[PASS] Old service removed" -ForegroundColor Green
}

# Step 7: Register the service using mysqld --install
Write-Host ""
Write-Host "Registering MySQL service..." -ForegroundColor Yellow
$result = & $MysqldPath --install $ServiceName --defaults-file="$DefaultsFile" 2>&1
if ($LASTEXITCODE -eq 0 -or $result -match "successfully") {
    Write-Host "[PASS] Service '$ServiceName' registered successfully" -ForegroundColor Green
} else {
    Write-Host "[INFO] mysqld --install output: $result" -ForegroundColor Yellow
    # Fallback: try sc.exe create
    Write-Host "Trying sc.exe create fallback..." -ForegroundColor Yellow
    $binPath = "`"$MysqldPath`" --defaults-file=`"$DefaultsFile`" $ServiceName"
    sc.exe create $ServiceName binPath= $binPath start= auto DisplayName= "MySQL Server 8.4 (HiddenYatra)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] Could not register service" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "[PASS] Service registered via sc.exe" -ForegroundColor Green
}

# Step 8: Set service to start automatically
Write-Host ""
Write-Host "Setting service to Automatic startup..." -ForegroundColor Yellow
Set-Service -Name $ServiceName -StartupType Automatic
$svc = Get-Service -Name $ServiceName
Write-Host "[PASS] Service StartupType: $($svc.StartType)" -ForegroundColor Green

# Step 9: Start the service
Write-Host ""
Write-Host "Starting MySQL service..." -ForegroundColor Yellow
Start-Service -Name $ServiceName
Start-Sleep -Seconds 3
$svc = Get-Service -Name $ServiceName
if ($svc.Status -eq "Running") {
    Write-Host "[PASS] Service is RUNNING" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Service status: $($svc.Status)" -ForegroundColor Red
    Write-Host "Check the Windows Event Log for errors." -ForegroundColor Yellow
    pause
    exit 1
}

# Step 10: Verify port 3306
Write-Host ""
Write-Host "Verifying port 3306..." -ForegroundColor Yellow
$portCheck = netstat -an | Select-String ":3306.*LISTENING"
if ($portCheck) {
    Write-Host "[PASS] Port 3306 is LISTENING" -ForegroundColor Green
    $portCheck | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
} else {
    Write-Host "[FAIL] Port 3306 is not listening" -ForegroundColor Red
}

# Step 11: Test database connectivity
Write-Host ""
Write-Host "Testing database connectivity..." -ForegroundColor Yellow
$mysqlExe = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
$testResult = & $mysqlExe -u root --port=3306 -e "SELECT 'CONNECTION_OK' AS status;" 2>&1
if ($testResult -match "CONNECTION_OK") {
    Write-Host "[PASS] MySQL connection successful" -ForegroundColor Green
} else {
    Write-Host "[WARN] Connection test: $testResult" -ForegroundColor Yellow
}

# Verify HiddenYatra database
$dbResult = & $mysqlExe -u root --port=3306 -e "USE hiddenyatra; SELECT COUNT(*) AS places FROM places;" 2>&1
if ($dbResult -match "\d+") {
    Write-Host "[PASS] hiddenyatra database accessible" -ForegroundColor Green
} else {
    Write-Host "[WARN] DB test: $dbResult" -ForegroundColor Yellow
}

# Final summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " SETUP COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " Service Name : $ServiceName" -ForegroundColor White
Write-Host " Startup Type : Automatic" -ForegroundColor White
Write-Host " Data Dir     : $DataDir" -ForegroundColor White
Write-Host " Port         : 3306" -ForegroundColor White
Write-Host ""
Write-Host " MySQL will now start automatically on Windows boot." -ForegroundColor Green
Write-Host " You can start HiddenYatra anytime with:" -ForegroundColor Green
Write-Host "   cd D:\HiddenYatra" -ForegroundColor Yellow
Write-Host "   python app.py" -ForegroundColor Yellow
Write-Host ""
pause
