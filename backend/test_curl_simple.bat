@echo off
echo Simple curl test for MiniTrack

REM Simple health check first
echo Testing server health...
curl -s http://localhost:8000/ | echo.

echo.
echo Testing video upload...
curl -X POST ^
  -F "file=@D:\Project\minitrack\source\external\2025_04_22 20_20.mp4" ^
  -F "debug_flag=true" ^
  http://localhost:8000/upload-video

pause