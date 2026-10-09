# MiniTrack Stop Script
# Stop running backend and web servers

Write-Host "Stopping MiniTrack..." -ForegroundColor Red
Write-Host ""

# Stop uvicorn (backend) processes
Write-Host "Stopping Backend Server..." -ForegroundColor Yellow
$uvicornProcesses = Get-Process -Name "python", "uvicorn" -ErrorAction SilentlyContinue | 
    Where-Object { $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*main_full*" }

if ($uvicornProcesses) {
    $uvicornProcesses | Stop-Process -Force
    Write-Host "   Backend server stopped" -ForegroundColor Green
} else {
    Write-Host "   No backend server running" -ForegroundColor Gray
}

# Stop npm/node (web) processes
Write-Host "Stopping Web Frontend..." -ForegroundColor Yellow
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue | 
    Where-Object { $_.Path -like "*minitrack\web*" -or $_.CommandLine -like "*react-scripts*" }

if ($nodeProcesses) {
    $nodeProcesses | Stop-Process -Force
    Write-Host "   Web frontend stopped" -ForegroundColor Green
} else {
    Write-Host "   No web server running" -ForegroundColor Gray
}

# Check and clean ports (8000, 3000)
Write-Host ""
Write-Host "Checking port status..." -ForegroundColor Yellow

# Check port 8000
$port8000 = netstat -ano | findstr :8000
if ($port8000) {
    Write-Host "   Port 8000 still in use" -ForegroundColor Yellow
    $pid = ($port8000 -split '\s+')[-1]
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Write-Host "   Port 8000 cleared" -ForegroundColor Green
}

# Check port 3000
$port3000 = netstat -ano | findstr :3000
if ($port3000) {
    Write-Host "   Port 3000 still in use" -ForegroundColor Yellow
    $pid = ($port3000 -split '\s+')[-1]
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Write-Host "   Port 3000 cleared" -ForegroundColor Green
}

# Clean up Jobs (for start-minitrack-simple.ps1)
$jobs = Get-Job -ErrorAction SilentlyContinue
if ($jobs) {
    Write-Host ""
    Write-Host "Cleaning background jobs..." -ForegroundColor Yellow
    $jobs | Stop-Job
    $jobs | Remove-Job
    Write-Host "   Background jobs cleaned" -ForegroundColor Green
}

Write-Host ""
Write-Host "MiniTrack stopped completely." -ForegroundColor Green
Write-Host ""