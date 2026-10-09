@echo off
echo =====================================
echo Verbose curl test with detailed output
echo =====================================

set VIDEO_PATH=D:\Project\minitrack\source\external\2025_04_22 20_20.mp4

echo Testing with verbose output and detailed headers...
echo.

curl -X POST ^
  -F "file=@%VIDEO_PATH%" ^
  -F "debug_flag=true" ^
  -H "Accept: application/json" ^
  -H "User-Agent: MiniTrack-Test/1.0" ^
  --verbose ^
  --include ^
  --max-time 120 ^
  --write-out "\n\n=== CURL STATISTICS ===\nTotal time: %%{time_total}s\nHTTP code: %%{http_code}\nUpload size: %%{size_upload} bytes\nDownload size: %%{size_download} bytes\n" ^
  http://localhost:8000/upload-video

echo.
echo Test completed.
pause