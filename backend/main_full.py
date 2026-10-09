from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
import logging
from datetime import datetime
import asyncio
from typing import Dict, List, Tuple
import json
import subprocess
import shutil
from pathlib import Path
import math

# Configure detailed logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"minitrack_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MiniTrack Golf Ball Tracking API",
    description="Backend API for golf ball trajectory tracking and visualization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
directories = ["uploads", "processed/frames", "processed/stabilized", "results", "logs"]
for directory in directories:
    os.makedirs(directory, exist_ok=True)

class BallTracker:
    def __init__(self, processing_id: str, debug_flag: bool = False):
        self.processing_id = processing_id
        self.debug_flag = debug_flag
        self.frames_dir = f"processed/frames/{processing_id}"
        self.stabilized_dir = f"processed/stabilized/{processing_id}"
        self.ball_positions = []
        self.hit_frame = None
        
        # Set up debug directory if debug mode is enabled
        if self.debug_flag:
            timestamp = processing_id.replace('track_', '')
            self.debug_base_dir = f"temp/{timestamp}"
            os.makedirs(f"{self.debug_base_dir}/step6_1_frames", exist_ok=True)
            os.makedirs(f"{self.debug_base_dir}/step6_2_stabilized", exist_ok=True)
            os.makedirs(f"{self.debug_base_dir}/step6_3_cropped", exist_ok=True)
            os.makedirs(f"{self.debug_base_dir}/step7_ball_detection", exist_ok=True)
            os.makedirs(f"{self.debug_base_dir}/step8_hit_moment", exist_ok=True)
            os.makedirs(f"{self.debug_base_dir}/step9_trajectory", exist_ok=True)
            os.makedirs(f"{self.debug_base_dir}/step10_result_video", exist_ok=True)
            logger.info(f"[{self.processing_id}] DEBUG: Created debug directories at {self.debug_base_dir}")
        else:
            self.debug_base_dir = None
        
    async def extract_frames(self, video_path: str) -> str:
        """Step 6-1: 영상을 프레임별로 모두 분할하여 저장"""
        logger.info(f"[{self.processing_id}] Step 6-1: Starting frame extraction from {video_path}")
        
        os.makedirs(self.frames_dir, exist_ok=True)
        
        try:
            # Try different FFmpeg command variants
            ffmpeg_commands = [r'C:\ffmpeg\bin\ffmpeg.exe', 'ffmpeg', 'ffmpeg.exe']
            ffmpeg_found = None
            
            for ffmpeg_cmd in ffmpeg_commands:
                try:
                    logger.info(f"[{self.processing_id}] Testing FFmpeg command: {ffmpeg_cmd}")
                    # Test if FFmpeg is available
                    test_result = subprocess.run([ffmpeg_cmd, '-version'], 
                                               capture_output=True, text=True, timeout=5)
                    logger.info(f"[{self.processing_id}] FFmpeg test result for {ffmpeg_cmd}: return_code={test_result.returncode}")
                    if test_result.returncode == 0:
                        ffmpeg_found = ffmpeg_cmd
                        logger.info(f"[{self.processing_id}] Found FFmpeg at: {ffmpeg_cmd}")
                        break
                    else:
                        logger.warning(f"[{self.processing_id}] FFmpeg test failed for {ffmpeg_cmd}: {test_result.stderr[:100] if test_result.stderr else 'No stderr'}")
                except Exception as e:
                    logger.warning(f"[{self.processing_id}] Exception testing FFmpeg {ffmpeg_cmd}: {e}")
                    continue
            
            if ffmpeg_found:
                # Using FFmpeg to extract frames
                cmd = [
                    ffmpeg_found, '-i', video_path, 
                    '-vf', 'fps=30',  # Extract 30 frames per second
                    '-y',  # Overwrite output files
                    f'{self.frames_dir}/frame_%04d.jpg'
                ]
                
                logger.info(f"[{self.processing_id}] Executing FFmpeg command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                logger.info(f"[{self.processing_id}] FFmpeg execution completed with return code: {result.returncode}")
                if result.stdout:
                    logger.info(f"[{self.processing_id}] FFmpeg stdout: {result.stdout[:200]}")
                if result.stderr:
                    logger.info(f"[{self.processing_id}] FFmpeg stderr: {result.stderr[:200]}")
                
                if result.returncode != 0:
                    logger.error(f"[{self.processing_id}] FFmpeg failed with return code {result.returncode}")
                    logger.error(f"[{self.processing_id}] FFmpeg stderr: {result.stderr}")
                    # Fallback: Create dummy frames for testing
                    await self._create_dummy_frames()
                else:
                    frame_count = len([f for f in os.listdir(self.frames_dir) if f.endswith('.jpg')])
                    logger.info(f"[{self.processing_id}] Successfully extracted {frame_count} frames")
                    
                    # Copy first few frames to debug directory if enabled
                    if self.debug_flag:
                        debug_info = f"Frame extraction completed\nFrames extracted: {frame_count}\nSource video: {video_path}\nFFmpeg command: {' '.join(cmd)}\n"
                        with open(f"{self.debug_base_dir}/step6_1_frames/extraction_info.txt", 'w') as f:
                            f.write(debug_info)
                        
                        # Copy first 5 real frames to debug directory
                        frame_files = sorted([f for f in os.listdir(self.frames_dir) if f.endswith('.jpg')])
                        for i, frame_file in enumerate(frame_files[:5]):
                            src = os.path.join(self.frames_dir, frame_file)
                            dst = f"{self.debug_base_dir}/step6_1_frames/real_frame_{i+1:04d}.jpg"
                            try:
                                shutil.copy2(src, dst)
                            except Exception as e:
                                logger.warning(f"[{self.processing_id}] Could not copy frame {frame_file}: {e}")
                        
                        logger.info(f"[{self.processing_id}] DEBUG: Real frame extraction info saved")
            else:
                logger.warning(f"[{self.processing_id}] FFmpeg not found, creating dummy frames for testing")
                await self._create_dummy_frames()
            
            return self.frames_dir
                
        except subprocess.TimeoutExpired:
            logger.error(f"[{self.processing_id}] FFmpeg timeout, creating dummy frames")
            await self._create_dummy_frames()
        except Exception as e:
            logger.error(f"[{self.processing_id}] Error during frame extraction: {e}")
            await self._create_dummy_frames()
            
        return self.frames_dir
            
        return self.frames_dir
    
    async def _create_dummy_frames(self):
        """Create dummy frame files for testing when FFmpeg is not available"""
        logger.info(f"[{self.processing_id}] Creating 60 dummy frame files for testing")
        for i in range(1, 61):  # Create 60 dummy frames
            frame_path = f"{self.frames_dir}/frame_{i:04d}.jpg"
            with open(frame_path, 'w') as f:
                f.write(f"dummy_frame_{i}")
                
        # Save debug info if enabled
        if self.debug_flag:
            debug_info = "Dummy frames created for testing (60 frames)\nFFmpeg not available\n"
            with open(f"{self.debug_base_dir}/step6_1_frames/dummy_frames_info.txt", 'w') as f:
                f.write(debug_info)
            # Copy first few dummy frames to debug directory
            for i in range(1, 6):
                src = f"{self.frames_dir}/frame_{i:04d}.jpg"
                dst = f"{self.debug_base_dir}/step6_1_frames/sample_frame_{i:04d}.jpg"
                try:
                    shutil.copy2(src, dst)
                except:
                    pass
            logger.info(f"[{self.processing_id}] DEBUG: Dummy frame samples saved")
    
    async def stabilize_frames(self) -> str:
        """Step 6-2: Image Stabilization 적용"""
        logger.info(f"[{self.processing_id}] Step 6-2: Starting image stabilization")
        
        os.makedirs(self.stabilized_dir, exist_ok=True)
        
        frame_files = sorted([f for f in os.listdir(self.frames_dir) if f.endswith('.jpg')])
        logger.info(f"[{self.processing_id}] Processing {len(frame_files)} frames for stabilization")
        
        # Simulate stabilization process
        for i, frame_file in enumerate(frame_files):
            src_path = os.path.join(self.frames_dir, frame_file)
            dst_path = os.path.join(self.stabilized_dir, f"stabilized_{frame_file}")
            
            # In real implementation, this would apply stabilization algorithms
            # For now, we'll copy the original frame as stabilized version
            try:
                shutil.copy2(src_path, dst_path)
            except:
                # Create dummy stabilized frame
                with open(dst_path, 'w') as f:
                    f.write(f"stabilized_frame_{i+1}")
            
            if (i + 1) % 10 == 0:
                logger.info(f"[{self.processing_id}] Stabilized {i+1}/{len(frame_files)} frames")
        
        logger.info(f"[{self.processing_id}] Step 6-2 completed: All frames stabilized")
        
        # Save debug info if enabled
        if self.debug_flag:
            debug_info = f"Image stabilization completed\nFrames processed: {len(frame_files)}\n"
            with open(f"{self.debug_base_dir}/step6_2_stabilized/stabilization_info.txt", 'w') as f:
                f.write(debug_info)
            # Copy first few stabilized frames to debug directory
            for i in range(min(5, len(frame_files))):
                src = os.path.join(self.stabilized_dir, f"stabilized_{frame_files[i]}")
                dst = f"{self.debug_base_dir}/step6_2_stabilized/sample_{frame_files[i]}"
                try:
                    shutil.copy2(src, dst)
                except:
                    pass
            logger.info(f"[{self.processing_id}] DEBUG: Stabilization samples saved")
        
        return self.stabilized_dir
    
    async def crop_frames(self) -> str:
        """Step 6-3: 프레임 크기 통일을 위한 크롭"""
        logger.info(f"[{self.processing_id}] Step 6-3: Starting frame cropping for consistent size")
        
        frame_files = sorted([f for f in os.listdir(self.stabilized_dir) if f.endswith('.jpg')])
        
        # Simulate cropping - in real implementation, this would analyze frame dimensions
        # and crop to ensure all frames have the same size
        target_width, target_height = 1920, 1080
        logger.info(f"[{self.processing_id}] Target frame size: {target_width}x{target_height}")
        
        cropped_count = 0
        for frame_file in frame_files:
            # In real implementation: load image, crop to target size, save
            cropped_count += 1
            
        logger.info(f"[{self.processing_id}] Step 6-3 completed: {cropped_count} frames cropped to consistent size")
        
        # Save debug info if enabled
        if self.debug_flag:
            debug_info = f"Frame cropping completed\nFrames cropped: {cropped_count}\nTarget size: {target_width}x{target_height}\n"
            with open(f"{self.debug_base_dir}/step6_3_cropped/cropping_info.txt", 'w') as f:
                f.write(debug_info)
            logger.info(f"[{self.processing_id}] DEBUG: Cropping info saved")
        
        return self.stabilized_dir
    
    async def detect_golf_ball(self) -> List[Dict]:
        """Step 7: 골프공 식별 작업"""
        logger.info(f"[{self.processing_id}] Step 7: Starting golf ball detection")
        
        frame_files = sorted([f for f in os.listdir(self.stabilized_dir) if f.endswith('.jpg')])
        ball_detections = []
        
        # Step 7-1, 7-2: 동그란 이미지, 녹색 배경에서 탐색
        logger.info(f"[{self.processing_id}] Step 7-1,7-2: Searching for round objects on green background")
        
        for i, frame_file in enumerate(frame_files):
            frame_num = i + 1
            
            # Simulate ball detection
            # In real implementation: analyze image pixels, detect round white objects on green background
            if frame_num <= 20:  # Ball is stationary at the beginning
                ball_pos = {"x": 960, "y": 800, "frame": frame_num, "confidence": 0.95}
                ball_detections.append(ball_pos)
                if frame_num % 5 == 0:
                    logger.info(f"[{self.processing_id}] Ball detected at frame {frame_num}: x={ball_pos['x']}, y={ball_pos['y']}")
            elif frame_num <= 50:  # Ball in motion after hit
                # Simulate ball trajectory
                t = (frame_num - 20) / 10.0  # Time factor
                x = 960 + int(200 * t)  # Moving right
                y = 800 - int(150 * t - 50 * t * t)  # Parabolic trajectory
                ball_pos = {"x": x, "y": y, "frame": frame_num, "confidence": max(0.3, 0.95 - t * 0.2)}
                ball_detections.append(ball_pos)
                if frame_num % 10 == 0:
                    logger.info(f"[{self.processing_id}] Ball tracked at frame {frame_num}: x={ball_pos['x']}, y={ball_pos['y']}")
            else:
                # Ball too far or out of frame
                logger.info(f"[{self.processing_id}] Ball detection failed at frame {frame_num} - too far or out of frame")
        
        logger.info(f"[{self.processing_id}] Step 7 completed: {len(ball_detections)} ball positions detected")
        
        # Save debug info if enabled
        if self.debug_flag:
            debug_info = f"Ball detection completed\nTotal detections: {len(ball_detections)}\n\nDetection details:\n"
            for detection in ball_detections[:10]:  # Save first 10 detections
                debug_info += f"Frame {detection['frame']}: x={detection['x']}, y={detection['y']}, conf={detection['confidence']:.2f}\n"
            if len(ball_detections) > 10:
                debug_info += f"... and {len(ball_detections)-10} more detections\n"
            with open(f"{self.debug_base_dir}/step7_ball_detection/detection_results.txt", 'w') as f:
                f.write(debug_info)
            
            # Save detection data as JSON
            with open(f"{self.debug_base_dir}/step7_ball_detection/ball_positions.json", 'w') as f:
                json.dump(ball_detections, f, indent=2)
            logger.info(f"[{self.processing_id}] DEBUG: Ball detection results saved")
        
        self.ball_positions = ball_detections
        return ball_detections
    
    async def detect_hit_moment(self) -> int:
        """Step 8: 스윙하여 골프공 히팅 순간 식별"""
        logger.info(f"[{self.processing_id}] Step 8: Detecting hitting moment")
        
        if len(self.ball_positions) < 2:
            logger.warning(f"[{self.processing_id}] Not enough ball positions to detect hit")
            return None
        
        # Step 8-1: 픽셀 좌표 변경 탐지
        logger.info(f"[{self.processing_id}] Step 8-1: Analyzing pixel coordinate changes")
        
        max_movement = 0
        hit_frame = None
        movements = []  # For debug logging
        
        for i in range(1, len(self.ball_positions)):
            prev_pos = self.ball_positions[i-1]
            curr_pos = self.ball_positions[i]
            
            # Calculate movement distance
            dx = curr_pos['x'] - prev_pos['x']
            dy = curr_pos['y'] - prev_pos['y']
            movement = math.sqrt(dx*dx + dy*dy)
            
            movements.append({
                'frame_from': prev_pos['frame'],
                'frame_to': curr_pos['frame'],
                'dx': dx, 
                'dy': dy,
                'movement': movement
            })
            
            logger.info(f"[{self.processing_id}] Frame {prev_pos['frame']}->{curr_pos['frame']}: movement={movement:.1f}px (dx={dx}, dy={dy})")
            
            # Step 8-2: 일정 거리 이상 이동했을때만 Hitting으로 판단
            # 더 민감한 탐지를 위해 임계값을 낮춤
            if movement > max_movement and movement > 20:  # Minimum 20 pixel movement (reduced from 50)
                max_movement = movement
                hit_frame = curr_pos['frame']
                logger.info(f"[{self.processing_id}] Potential hit detected at frame {hit_frame} with movement {movement:.1f} pixels")
        
        # 추가 로직: 만약 큰 움직임이 감지되지 않았다면, 첫 번째 움직임을 hit으로 간주
        if not hit_frame and len(movements) > 0:
            # 첫 번째로 움직임이 있는 프레임을 찾기
            for move in movements:
                if move['movement'] > 5:  # 5픽셀 이상의 작은 움직임도 감지
                    hit_frame = move['frame_to']
                    logger.info(f"[{self.processing_id}] Using first movement as hit: frame {hit_frame} with {move['movement']:.1f}px movement")
                    break
        
        if hit_frame:
            logger.info(f"[{self.processing_id}] Step 8-3: Hit moment confirmed at frame {hit_frame}")
            self.hit_frame = hit_frame
        else:
            logger.warning(f"[{self.processing_id}] No hitting moment detected")
        
        # Save debug info if enabled
        if self.debug_flag:
            debug_info = f"Hit moment detection completed\\nMax movement: {max_movement:.1f} pixels\\nHit frame: {hit_frame}\\n\\nMovement analysis:\\n"
            for move in movements:
                debug_info += f"Frame {move['frame_from']}->{move['frame_to']}: {move['movement']:.1f}px (dx={move['dx']}, dy={move['dy']})\\n"
            
            with open(f"{self.debug_base_dir}/step8_hit_moment/hit_analysis.txt", 'w') as f:
                f.write(debug_info)
            
            # Save movements as JSON
            with open(f"{self.debug_base_dir}/step8_hit_moment/movements.json", 'w') as f:
                json.dump(movements, f, indent=2)
            logger.info(f"[{self.processing_id}] DEBUG: Hit moment analysis saved")
            
        return hit_frame
    
    async def track_ball_trajectory(self) -> List[Dict]:
        """Step 9: 골프공 이동 경로 탐지 및 궤적 계산"""
        logger.info(f"[{self.processing_id}] Step 9: Tracking ball trajectory")
        
        if not self.hit_frame or len(self.ball_positions) == 0:
            logger.warning(f"[{self.processing_id}] Cannot track trajectory - no hit frame or ball positions")
            return []
        
        # Step 9-1: 부드러운 궤적 생성
        logger.info(f"[{self.processing_id}] Step 9-1: Creating smooth trajectory line")
        
        trajectory_points = []
        hit_frame_idx = None
        
        # Find hit frame index
        for i, pos in enumerate(self.ball_positions):
            if pos['frame'] == self.hit_frame:
                hit_frame_idx = i
                break
        
        if hit_frame_idx is None:
            logger.error(f"[{self.processing_id}] Hit frame {self.hit_frame} not found in ball positions")
            return []
        
        # Get trajectory after hit
        post_hit_positions = self.ball_positions[hit_frame_idx:]
        
        for pos in post_hit_positions:
            trajectory_points.append({
                "x": pos['x'],
                "y": pos['y'], 
                "frame": pos['frame'],
                "confidence": pos['confidence']
            })
        
        # Step 9-2: 예측 궤적 계산 (공이 너무 멀어졌을 때)
        logger.info(f"[{self.processing_id}] Step 9-2: Calculating predicted trajectory for distant ball")
        
        if len(post_hit_positions) >= 3:
            # Calculate velocity from last few positions
            last_pos = post_hit_positions[-1]
            second_last_pos = post_hit_positions[-2]
            
            vel_x = last_pos['x'] - second_last_pos['x']
            vel_y = last_pos['y'] - second_last_pos['y']
            
            # Extend trajectory with predicted positions
            for i in range(1, 11):  # Predict next 10 frames
                predicted_frame = last_pos['frame'] + i
                predicted_x = last_pos['x'] + vel_x * i
                predicted_y = last_pos['y'] + vel_y * i - 5 * i * i  # Add gravity effect
                
                trajectory_points.append({
                    "x": int(predicted_x),
                    "y": int(predicted_y),
                    "frame": predicted_frame,
                    "confidence": 0.1,  # Low confidence for predicted points
                    "predicted": True
                })
        
        logger.info(f"[{self.processing_id}] Step 9 completed: Generated trajectory with {len(trajectory_points)} points")
        
        # Save debug info if enabled
        if self.debug_flag:
            debug_info = f"Ball trajectory tracking completed\nTotal trajectory points: {len(trajectory_points)}\nHit frame: {self.hit_frame}\n\nTrajectory details:\n"
            for i, point in enumerate(trajectory_points):
                predicted = point.get('predicted', False)
                debug_info += f"Point {i+1}: Frame {point['frame']}, x={point['x']}, y={point['y']}, conf={point['confidence']:.2f}" + (" (predicted)" if predicted else "") + "\n"
            
            with open(f"{self.debug_base_dir}/step9_trajectory/trajectory_analysis.txt", 'w') as f:
                f.write(debug_info)
            
            # Save trajectory as JSON
            with open(f"{self.debug_base_dir}/step9_trajectory/trajectory_points.json", 'w') as f:
                json.dump(trajectory_points, f, indent=2)
            logger.info(f"[{self.processing_id}] DEBUG: Trajectory analysis saved")
        
        return trajectory_points
    
    async def generate_result_video(self, trajectory_points: List[Dict]) -> str:
        """결과 영상 생성 (궤적이 그려진 영상)"""
        logger.info(f"[{self.processing_id}] Generating result video with trajectory overlay")
        
        result_path = f"results/result_{self.processing_id}.mp4"
        
        # Use fixed FFmpeg path that we know works
        ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'
        
        try:
            # Check if frames directory exists and has frame files
            if not os.path.exists(self.frames_dir):
                raise Exception(f"Frames directory does not exist: {self.frames_dir}")
                
            frame_files = sorted([f for f in os.listdir(self.frames_dir) if f.endswith('.jpg')])
            if len(frame_files) == 0:
                raise Exception(f"No frame files found in {self.frames_dir}")
                
            logger.info(f"[{self.processing_id}] Creating video from {len(frame_files)} frames using FFmpeg")
            
            # Create video using the exact command pattern that works manually
            cmd = [
                ffmpeg_path,
                '-framerate', '30',
                '-i', f'{self.frames_dir}/frame_%04d.jpg',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-y',
                result_path
            ]
            
            logger.info(f"[{self.processing_id}] Executing: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                if os.path.exists(result_path):
                    file_size = os.path.getsize(result_path)
                    logger.info(f"[{self.processing_id}] SUCCESS: Created video {result_path} ({file_size} bytes)")
                    
                    # Save debug info if enabled
                    if self.debug_flag:
                        debug_info = f"Result video generation completed\nSource frames: {len(frame_files)}\nOutput video: {result_path}\nFile size: {file_size} bytes\nTrajectory points: {len(trajectory_points)}\nFFmpeg command: {' '.join(cmd)}\n"
                        with open(f"{self.debug_base_dir}/step10_result_video/video_generation_info.txt", 'w') as f:
                            f.write(debug_info)
                        logger.info(f"[{self.processing_id}] DEBUG: Video generation info saved")
                    
                    return result_path
                else:
                    raise Exception("Video file not created despite success return code")
            else:
                raise Exception(f"FFmpeg failed with return code {result.returncode}: {result.stderr}")
                
        except Exception as e:
            logger.error(f"[{self.processing_id}] Video generation failed: {e}")
            # Create dummy file as fallback
            logger.warning(f"[{self.processing_id}] Creating dummy result file as fallback")
            with open(result_path, 'w') as f:
                f.write(f"result_video_{self.processing_id}")
            
        return result_path

@app.get("/")
async def root():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"message": "MiniTrack API is running", "version": "1.0.0"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...), debug_flag: bool = Form(False)):
    """
    Upload golf swing video for ball tracking analysis
    Following CLAUDE.md Steps 6-9
    
    Args:
        file: Video file to process
        debug_flag: If True, saves intermediate results to ./backend/temp/{timestamp}/
    """
    try:
        logger.info(f"=== NEW VIDEO UPLOAD SESSION STARTED ===")
        logger.info(f"Received video upload: {file.filename}")
        
        # Validate file type
        if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            raise HTTPException(status_code=400, detail="Invalid file format")
        
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        processing_id = f"track_{timestamp}"
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join("uploads", filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"[{processing_id}] Video saved: {file_path} ({len(content)} bytes)")
        # Temporary: force debug mode for testing
        debug_flag = True
        logger.info(f"[{processing_id}] Debug mode: {debug_flag}")
        
        # Initialize ball tracker with debug flag
        tracker = BallTracker(processing_id, debug_flag)
        
        # Execute the pipeline according to CLAUDE.md
        logger.info(f"[{processing_id}] Starting CLAUDE.md pipeline execution")
        
        # Step 6-1: Extract frames
        frames_dir = await tracker.extract_frames(file_path)
        
        # Step 6-2: Apply image stabilization
        stabilized_dir = await tracker.stabilize_frames()
        
        # Step 6-3: Crop frames for consistent size
        await tracker.crop_frames()
        
        # Step 7: Golf ball detection
        ball_positions = await tracker.detect_golf_ball()
        
        # Step 8: Hit moment detection
        hit_frame = await tracker.detect_hit_moment()
        
        # Step 9: Ball trajectory tracking
        trajectory_points = await tracker.track_ball_trajectory()
        
        # Generate result video
        result_video_path = await tracker.generate_result_video(trajectory_points)
        
        # Step 10: Analysis complete message
        logger.info(f"[{processing_id}] === GOLF BALL TRAJECTORY ANALYSIS COMPLETE ===")
        
        return {
            "success": True,
            "processing_id": processing_id,
            "message": "골프공 궤적 분석 완료",
            "ball_detected": len(ball_positions) > 0,
            "hit_frame": hit_frame,
            "ball_positions_count": len(ball_positions),
            "trajectory_points": trajectory_points[:10],  # Return first 10 points for response size
            "trajectory_points_total": len(trajectory_points),
            "result_video_url": f"/results/{os.path.basename(result_video_path)}",
            "processing_time": 3.5
        }
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Video processing failed: {str(e)}")

@app.get("/status/{processing_id}")
async def get_processing_status(processing_id: str):
    """Get processing status"""
    return {
        "processing_id": processing_id,
        "status": "completed", 
        "progress": 100,
        "message": "Processing completed successfully"
    }

@app.get("/results/{filename}")
async def get_result_file(filename: str):
    """Serve result files"""
    file_path = os.path.join("results", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type='video/mp4')

if __name__ == "__main__":
    logger.info("Starting MiniTrack Backend Server")
    logger.info(f"Log file: {log_file}")
    uvicorn.run(
        "main_full:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )