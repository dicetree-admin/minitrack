import os
import subprocess

# Test video generation manually
processing_id = "track_20250810_215913"
frames_dir = f"processed/frames/{processing_id}"
result_path = f"results/debug_result_{processing_id}.mp4"

print(f"Testing video generation for: {processing_id}")
print(f"Frames directory: {frames_dir}")
print(f"Frames directory exists: {os.path.exists(frames_dir)}")

if os.path.exists(frames_dir):
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    print(f"Found {len(frame_files)} frame files")
    print(f"First few frames: {frame_files[:5]}")
    
    # Test FFmpeg path
    ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'
    print(f"FFmpeg path: {ffmpeg_path}")
    print(f"FFmpeg exists: {os.path.exists(ffmpeg_path)}")
    
    # Test FFmpeg version
    try:
        test_result = subprocess.run([ffmpeg_path, '-version'], 
                                   capture_output=True, text=True, timeout=5)
        print(f"FFmpeg version test return code: {test_result.returncode}")
        if test_result.returncode == 0:
            print("FFmpeg is working!")
            
            # Try to create video
            cmd = [
                ffmpeg_path,
                '-framerate', '30',
                '-i', f'{frames_dir}/frame_%04d.jpg',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-y',
                result_path
            ]
            
            print(f"Executing: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            print(f"Video creation return code: {result.returncode}")
            
            if result.returncode == 0:
                if os.path.exists(result_path):
                    file_size = os.path.getsize(result_path)
                    print(f"SUCCESS: Created video {result_path} ({file_size} bytes)")
                else:
                    print("ERROR: Video file not created despite success return code")
            else:
                print(f"ERROR: FFmpeg failed")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                
        else:
            print(f"FFmpeg version test failed: {test_result.stderr}")
            
    except Exception as e:
        print(f"Exception during FFmpeg test: {e}")
        
else:
    print("ERROR: Frames directory does not exist")