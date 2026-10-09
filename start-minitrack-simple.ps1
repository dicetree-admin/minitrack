# MiniTrack Simple Launch Script
# Run backend and web in one window (simple version)

Write-Host "Starting MiniTrack..." -ForegroundColor Green

# Run backend (background)
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Start-Job -ScriptBlock {
    cd "D:\Project\minitrack"
    & ".\venv\Scripts\activate.ps1"
    cd backend
    uvicorn main_full:app --reload --host 0.0.0.0 --port 8000
} | Out-Null

# Wait 3 seconds
Start-Sleep -Seconds 3

# Run web frontend (background)
Write-Host "Starting Web Frontend..." -ForegroundColor Yellow
Start-Job -ScriptBlock {
    cd "D:\Project\minitrack\web"
    npm start
} | Out-Null

# Display access info
Write-Host ""
Write-Host "MiniTrack Started!" -ForegroundColor Green
Write-Host "   Web UI: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# Open browser after 5 seconds
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"

# Monitor job status
Write-Host "Servers running... (Press Ctrl+C to stop)" -ForegroundColor Yellow
while ($true) {
    Get-Job | Format-Table -AutoSize
    Start-Sleep -Seconds 5
}