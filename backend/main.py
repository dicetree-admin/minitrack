from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
import logging
from datetime import datetime
from typing import List

from services.video_processor import VideoProcessor
from services.ball_tracker import BallTracker
from models.response_models import TrackingResponse, ProcessingStatus

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MiniTrack Golf Ball Tracking API",
    description="Backend API for golf ball trajectory tracking and visualization",
    version="1.0.0"
)

# CORS middleware for React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
video_processor = VideoProcessor()
ball_tracker = BallTracker()

# Create directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("results", exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "MiniTrack API is running", "version": "1.0.0"}

@app.post("/upload-video", response_model=TrackingResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Upload golf swing video for ball tracking analysis
    
    Flow according to CLAUDE.md:
    1. Save uploaded video
    2. Extract frames from video
    3. Apply image stabilization
    4. Crop frames to consistent size
    5. Detect golf ball in frames
    6. Track ball trajectory
    7. Generate visualization
    """
    try:
        logger.info(f"Received video upload: {file.filename}")
        
        # Validate file type
        if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a video file.")
        
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join("uploads", filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Video saved to: {file_path}")
        
        # Process video through the pipeline
        processing_id = f"track_{timestamp}"
        
        # Step 1: Extract frames
        logger.info("Starting frame extraction...")
        frames_dir = await video_processor.extract_frames(file_path, processing_id)
        
        # Step 2: Apply image stabilization
        logger.info("Applying image stabilization...")
        stabilized_dir = await video_processor.stabilize_frames(frames_dir, processing_id)
        
        # Step 3: Detect and track golf ball
        logger.info("Starting golf ball detection and tracking...")
        tracking_result = await ball_tracker.track_ball_trajectory(stabilized_dir, processing_id)
        
        # Step 4: Generate result video with trajectory
        logger.info("Generating result video...")
        result_video_path = await video_processor.create_result_video(
            stabilized_dir, 
            tracking_result.trajectory_points,
            processing_id
        )
        
        logger.info(f"Ball tracking completed successfully: {processing_id}")
        
        return TrackingResponse(
            success=True,
            processing_id=processing_id,
            message="골프공 궤적 분석 완료",
            ball_detected=tracking_result.ball_detected,
            hit_frame=tracking_result.hit_frame,
            trajectory_points=tracking_result.trajectory_points,
            result_video_url=f"/results/{os.path.basename(result_video_path)}",
            processing_time=tracking_result.processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video processing failed: {str(e)}")

@app.get("/status/{processing_id}")
async def get_processing_status(processing_id: str):
    """Get processing status for a given processing ID"""
    # This would typically check a database or cache for status
    return ProcessingStatus(
        processing_id=processing_id,
        status="completed",
        progress=100,
        message="Processing completed successfully"
    )

@app.get("/results/{filename}")
async def get_result_file(filename: str):
    """Serve processed result files"""
    file_path = os.path.join("results", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type='video/mp4')

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )