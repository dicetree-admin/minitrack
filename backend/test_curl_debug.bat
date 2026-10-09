@echo off
echo =====================================
echo Windows curl Debug Test for MiniTrack
echo =====================================

set VIDEO_PATH=D:\Project\minitrack\source\external\2025_04_22 20_20.mp4
set SERVER_URL=http://localhost:8000/upload-video

echo.
echo Testing video upload with debug_flag=true
echo Video: %VIDEO_PATH%
echo Server: %SERVER_URL%
echo.

REM Check if video file exists
if not exist "%VIDEO_PATH%" (
    echo ERROR: Video file not found at %VIDEO_PATH%
    echo Please check the video file path.
    pause
    exit /b 1
)

echo Video file found. Size:
for %%A in ("%VIDEO_PATH%") do echo %%~zA bytes

echo.
echo Sending curl request...
echo.

REM Execute curl command with multipart form data
curl -X POST ^
  -F "file=@%VIDEO_PATH%" ^
  -F "debug_flag=true" ^
  -H "Accept: application/json" ^
  --progress-bar ^
  --max-time 120 ^
  %SERVER_URL%

echo.
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✓ Request completed successfully!
    echo.
    echo Check debug output at:
    echo D:\Project\minitrack\backend\temp\
    echo.
    echo Check server logs at:
    echo D:\Project\minitrack\backend\logs\
) else (
    echo ✗ Request failed with error code: %ERRORLEVEL%
    echo.
    echo Common issues:
    echo - Backend server not running ^(python main_full.py^)
    echo - Video file path incorrect
    echo - Network/firewall issues
)

echo.
pause