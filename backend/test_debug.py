import requests
import os

def test_debug_mode():
    # Test video file path
    video_path = r"D:\Project\minitrack\source\external\2025_04_22 20_20.mp4"
    
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    print(f"Testing debug mode with video: {video_path}")
    print(f"File size: {os.path.getsize(video_path)} bytes")
    
    # Prepare the request
    url = "http://localhost:8000/upload-video"
    
    try:
        with open(video_path, 'rb') as video_file:
            files = {'file': ('test_video.mp4', video_file, 'video/mp4')}
            data = {'debug_flag': True}  # Use boolean instead of string
            
            print("Sending request with debug_flag=True...")
            response = requests.post(url, files=files, data=data, timeout=60)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("\n✅ Debug mode test successful!")
                print("Check the following directories for debug output:")
                print("- D:\\Project\\minitrack\\backend\\temp\\")
                print("- D:\\Project\\minitrack\\backend\\logs\\minitrack_20250810.log")
            else:
                print(f"\n❌ Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Error sending request: {e}")

if __name__ == "__main__":
    test_debug_mode()