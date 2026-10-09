import subprocess
import os

# Test FFmpeg directly
ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'
test_video = r'D:\Project\minitrack\source\external\2025_04_22 20_20.mp4'

print(f'Testing FFmpeg at: {ffmpeg_path}')
print(f'FFmpeg exists: {os.path.exists(ffmpeg_path)}')

if os.path.exists(test_video):
    print(f'Test video exists: {test_video}')
    
    # Test FFmpeg version
    try:
        result = subprocess.run([ffmpeg_path, '-version'], capture_output=True, text=True, timeout=5)
        print(f'FFmpeg version check return code: {result.returncode}')
        if result.stdout:
            print(f'FFmpeg version output (first line): {result.stdout.split("\n")[0]}')
    except Exception as e:
        print(f'FFmpeg version test failed: {e}')
        
    # Test frame extraction
    try:
        test_dir = 'test_frames'
        os.makedirs(test_dir, exist_ok=True)
        
        cmd = [ffmpeg_path, '-i', test_video, '-vf', 'fps=1', '-t', '2', '-y', f'{test_dir}/test_frame_%03d.jpg']
        print(f'Testing frame extraction command')
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(f'Frame extraction return code: {result.returncode}')
        if result.returncode != 0:
            print(f'FFmpeg stderr: {result.stderr}')
        else:
            frames = [f for f in os.listdir(test_dir) if f.endswith('.jpg')]
            print(f'Extracted frames: {len(frames)} files')
            
    except Exception as e:
        print(f'Frame extraction test failed: {e}')
else:
    print('Test video not found')