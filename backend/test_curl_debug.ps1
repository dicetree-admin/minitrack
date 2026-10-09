Write-Host "======================================" -ForegroundColor Green
Write-Host "PowerShell curl Debug Test for MiniTrack" -ForegroundColor Green  
Write-Host "======================================" -ForegroundColor Green

$videoPath = "D:\Project\minitrack\source\external\2025_04_22 20_20.mp4"
$serverUrl = "http://localhost:8000/upload-video"

Write-Host ""
Write-Host "Testing video upload with debug_flag=true" -ForegroundColor Yellow
Write-Host "Video: $videoPath" -ForegroundColor Cyan
Write-Host "Server: $serverUrl" -ForegroundColor Cyan
Write-Host ""

# Check if video file exists
if (!(Test-Path $videoPath)) {
    Write-Host "ERROR: Video file not found at $videoPath" -ForegroundColor Red
    Write-Host "Please check the video file path." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$fileSize = (Get-Item $videoPath).Length
Write-Host "Video file found. Size: $fileSize bytes" -ForegroundColor Green
Write-Host ""
Write-Host "Sending curl request..." -ForegroundColor Yellow
Write-Host ""

try {
    # Execute curl command
    $response = curl -X POST `
        -F "file=@$videoPath" `
        -F "debug_flag=true" `
        -H "Accept: application/json" `
        --progress-bar `
        --max-time 120 `
        $serverUrl
        
    Write-Host ""
    Write-Host $response -ForegroundColor White
    Write-Host ""
    Write-Host "✓ Request completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check debug output at:" -ForegroundColor Cyan
    Write-Host "D:\Project\minitrack\backend\temp\" -ForegroundColor White
    Write-Host ""
    Write-Host "Check server logs at:" -ForegroundColor Cyan  
    Write-Host "D:\Project\minitrack\backend\logs\" -ForegroundColor White
}
catch {
    Write-Host "✗ Request failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "- Backend server not running (python main_full.py)" -ForegroundColor White
    Write-Host "- Video file path incorrect" -ForegroundColor White
    Write-Host "- Network/firewall issues" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"