from pydantic import BaseModel
from typing import List, Optional, Tuple
from enum import Enum

class ProcessingStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TrajectoryPoint(BaseModel):
    """Single point in ball trajectory"""
    frame_number: int
    x: float
    y: float
    confidence: float
    timestamp: float

class BallDetectionResult(BaseModel):
    """Result of ball detection in a single frame"""
    frame_number: int
    detected: bool
    x: Optional[float] = None
    y: Optional[float] = None
    confidence: Optional[float] = None
    bbox: Optional[Tuple[float, float, float, float]] = None

class TrackingResult(BaseModel):
    """Complete ball tracking result"""
    ball_detected: bool
    hit_frame: Optional[int] = None
    trajectory_points: List[TrajectoryPoint] = []
    total_frames: int
    processing_time: float
    confidence_score: float

class TrackingResponse(BaseModel):
    """API response for ball tracking"""
    success: bool
    processing_id: str
    message: str
    ball_detected: bool
    hit_frame: Optional[int] = None
    trajectory_points: List[TrajectoryPoint] = []
    result_video_url: Optional[str] = None
    processing_time: Optional[float] = None

class ProcessingStatus(BaseModel):
    """Processing status response"""
    processing_id: str
    status: ProcessingStatusEnum
    progress: int  # 0-100
    message: str
    current_step: Optional[str] = None