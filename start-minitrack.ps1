# MiniTrack Integrated Launch Script
# Run backend and web frontend simultaneously

Write-Host "Starting MiniTrack..." -ForegroundColor Green
Write-Host ""

# Set project root directory
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Run backend server (in new window)
Write-Host "Starting Backend Server... (port 8000)" -ForegroundColor Yellow
$backendScript = @"
cd '$projectRoot'
& '.\venv\Scripts\activate.ps1'
cd backend
Write-Host 'Backend server running at http://localhost:8000' -ForegroundColor Green
Write-Host 'API Docs: http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host ''
uvicorn main_full:app --reload --host 0.0.0.0 --port 8000
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait for backend to start
Start-Sleep -Seconds 3

# Run web frontend (in new window)
Write-Host "Starting Web Frontend... (port 3000)" -ForegroundColor Yellow
$webScript = @"
cd '$projectRoot\web'
Write-Host 'Web application running at http://localhost:3000' -ForegroundColor Green
Write-Host ''
npm start
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $webScript

# Display info in main window
Write-Host ""
Write-Host "MiniTrack started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Access Info:" -ForegroundColor Cyan
Write-Host "   - Web UI: http://localhost:3000" -ForegroundColor White
Write-Host "   - API Server: http://localhost:8000" -ForegroundColor White
Write-Host "   - API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "To stop, press Ctrl+C in each PowerShell window." -ForegroundColor Yellow
Write-Host ""

# Auto-open browser (after 5 seconds)
Write-Host "Opening web browser in 5 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"

# Keep main window open
Write-Host "Main Console - Log Monitoring" -ForegroundColor Magenta
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")