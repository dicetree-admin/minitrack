from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import logging
from datetime import datetime
import asyncio
from typing import Dict, List

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

# Create directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("results", exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "MiniTrack API is running", "version": "1.0.0"}

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload golf swing video for ball tracking analysis
    Simplified version for testing without heavy dependencies
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
        
        # Simulate processing time
        processing_id = f"track_{timestamp}"
        
        # Simulate processing stages
        logger.info("Simulating video processing...")
        await asyncio.sleep(1)  # Simulate processing time
        
        logger.info(f"Ball tracking completed successfully: {processing_id}")
        
        # Return simplified response
        return {
            "success": True,
            "processing_id": processing_id,
            "message": "골프공 궤적 분석 완료",
            "ball_detected": True,
            "hit_frame": 25,
            "trajectory_points": [
                {"x": 100, "y": 200, "frame": 20},
                {"x": 150, "y": 180, "frame": 25},
                {"x": 200, "y": 160, "frame": 30},
                {"x": 250, "y": 140, "frame": 35},
                {"x": 300, "y": 120, "frame": 40}
            ],
            "result_video_url": f"/results/demo_result_{processing_id}.mp4",
            "processing_time": 1.5
        }
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video processing failed: {str(e)}")

@app.get("/status/{processing_id}")
async def get_processing_status(processing_id: str):
    """Get processing status for a given processing ID"""
    return {
        "processing_id": processing_id,
        "status": "completed",
        "progress": 100,
        "message": "Processing completed successfully"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )