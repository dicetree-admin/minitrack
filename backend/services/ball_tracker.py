import cv2
import numpy as np
import os
import logging
from typing import List, Tuple, Optional, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import math
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import euclidean

from models.response_models import TrackingResult, TrajectoryPoint, BallDetectionResult

logger = logging.getLogger(__name__)

class BallTracker:
    """
    Golf ball tracking service implementing the algorithm described in CLAUDE.md
    
    Steps 7-9 from CLAUDE.md:
    7) 골프공 식별 작업
    8) 스윙하여 골프공 히팅 순간 식별  
    9) 골프공 이동 경로 탐지
    """
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Ball detection parameters
        self.ball_min_radius = 5
        self.ball_max_radius = 50
        self.ball_color_ranges = [
            # White ball color ranges in HSV
            ([0, 0, 200], [180, 30, 255]),    # Bright white
            ([0, 0, 150], [180, 50, 255]),    # Off-white
        ]
        
        # Movement detection parameters
        self.min_movement_distance = 10  # Minimum distance to consider as movement
        self.max_trajectory_gap = 50     # Maximum gap between trajectory points
        self.trajectory_smoothing_factor = 0.3
        
    async def track_ball_trajectory(self, frames_dir: str, processing_id: str) -> TrackingResult:
        """
        Main ball tracking pipeline
        Implements CLAUDE.md Steps 7-9
        """
        start_time = asyncio.get_event_loop().time()
        
        def _track_ball():
            frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
            total_frames = len(frame_files)
            
            logger.info(f"Starting ball tracking for {total_frames} frames")
            
            # Step 7: Detect golf ball in frames
            logger.info("Step 7: Golf ball detection")
            ball_detections = self._detect_ball_in_frames(frames_dir, frame_files)
            
            # Step 8: Identify hitting moment
            logger.info("Step 8: Identifying hit moment")
            hit_frame = self._identify_hit_moment(ball_detections)
            
            # Step 9: Track ball trajectory
            logger.info("Step 9: Tracking ball trajectory")
            trajectory_points = self._track_trajectory(ball_detections, hit_frame, total_frames)
            
            # Calculate confidence score
            detected_frames = sum(1 for detection in ball_detections if detection.detected)
            confidence_score = detected_frames / total_frames if total_frames > 0 else 0.0
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return TrackingResult(
                ball_detected=len(trajectory_points) > 0,
                hit_frame=hit_frame,
                trajectory_points=trajectory_points,
                total_frames=total_frames,
                processing_time=processing_time,
                confidence_score=confidence_score
            )
        
        result = await asyncio.get_event_loop().run_in_executor(
            self.executor, _track_ball
        )
        
        return result
    
    def _detect_ball_in_frames(self, frames_dir: str, frame_files: List[str]) -> List[BallDetectionResult]:
        """
        CLAUDE.md Step 7: 저장된 Stabilization 프레임 이미지에서 프레임을 뒤로 이동해가며 골프공 식별 작업이 진행됨
        7-1) 골프공은 일반적으로 동그란 이미지를 가지고 있음
        7-2) 골프공은 녹색 풀 또는 녹색 메트 바닥에 놓고 치므로, 이미지 하단에 녹색 내 동그란 이미지를 우선 탐색해야 함
        7-3) 그러나 골프공에 음영이 질 경우, 동그란 이미지로 인식이 안될 확률이 높으니 이를 감안해서 찾을 수 있는 로직이 필요함
        7-4) 골프공이 식별되면 골프공의 이미지 내 좌표를 log에 출력. 만약 골프공을 찾지 못한다면 마찬가지로 Ball detectaion fail 로 로깅 출력 필요
        """
        logger.info("=" * 50)
        logger.info("CLAUDE.md Step 7: 저장된 Stabilization 프레임 이미지에서 골프공 식별 작업")
        logger.info("=" * 50)
        
        detections = []
        
        logger.info(f"총 {len(frame_files)}개 프레임에서 골프공 식별을 시작합니다.")
        logger.info("CLAUDE.md Step 7: 프레임을 뒤로 이동해가며 골프공 식별 작업이 진행됨")
        
        # 프레임을 뒤로 이동해가며 처리 (역순으로 처리)
        for i in range(len(frame_files) - 1, -1, -1):
            frame_file = frame_files[i]
            frame_path = os.path.join(frames_dir, frame_file)
            frame = cv2.imread(frame_path)
            
            if frame is None:
                logger.warning(f"프레임을 읽을 수 없습니다: {frame_file}")
                detections.insert(0, BallDetectionResult(frame_number=i, detected=False))
                continue
            
            logger.debug(f"Step 7 처리 중: Frame {i} ({frame_file}) - 뒤에서부터 순차 처리")
            
            # CLAUDE.md 7-2: 이미지 하단에 녹색 내 동그란 이미지를 우선 탐색
            height, width = frame.shape[:2]
            roi = frame[height//2:height, :]  # 하단 절반 영역 집중 탐색
            
            ball_detection = self._detect_ball_in_frame_advanced(roi, i, height//2, frame_file)
            
            # CLAUDE.md 7-4: 골프공 좌표 로깅 또는 Ball detection fail 로깅
            if ball_detection.detected:
                logger.info(f"Step 7-4 SUCCESS: Frame {i} ({frame_file})")
                logger.info(f"  ✓ 골프공 좌표: ({ball_detection.x:.1f}, {ball_detection.y:.1f})")
                logger.info(f"  ✓ 신뢰도: {ball_detection.confidence:.3f}")
                if ball_detection.bbox:
                    x1, y1, x2, y2 = ball_detection.bbox
                    logger.info(f"  ✓ 경계박스: ({x1:.1f}, {y1:.1f}) - ({x2:.1f}, {y2:.1f})")
            else:
                logger.info(f"Step 7-4 FAIL: Frame {i} ({frame_file}) - Ball detection fail")
            
            detections.insert(0, ball_detection)
            
            # 진행률 표시
            if (len(frame_files) - i) % 50 == 0:
                processed = len(frame_files) - i
                detected_count = sum(1 for d in detections if d.detected)
                logger.info(f"Step 7 진행률: {processed}/{len(frame_files)} 처리완료, 감지성공: {detected_count}개")
        
        detected_count = sum(1 for d in detections if d.detected)
        success_rate = (detected_count / len(detections)) * 100 if detections else 0
        
        logger.info("=" * 50)
        logger.info("Step 7 완료 - 골프공 식별 작업 결과:")
        logger.info(f"  - 처리된 프레임: {len(detections)}개")
        logger.info(f"  - 골프공 감지 성공: {detected_count}개")
        logger.info(f"  - 감지 성공률: {success_rate:.1f}%")
        logger.info("=" * 50)
        
        return detections
    
    def _detect_ball_in_frame(self, frame: np.ndarray, frame_number: int, y_offset: int = 0) -> BallDetectionResult:
        """
        Detect golf ball in a single frame
        Uses multiple detection methods for robustness
        """
        candidates = []
        
        # Method 1: Circle detection using HoughCircles
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=30,
            param1=50,
            param2=30,
            minRadius=self.ball_min_radius,
            maxRadius=self.ball_max_radius
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                x, y, r = circle
                confidence = self._calculate_ball_confidence(frame, x, y, r)
                candidates.append((x, y + y_offset, confidence, r))
        
        # Method 2: Color-based detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        for color_range in self.ball_color_ranges:
            lower, upper = color_range
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 50:  # Too small to be a golf ball
                    continue
                
                # Check if contour is roughly circular
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue
                
                circularity = 4 * math.pi * area / (perimeter * perimeter)
                
                if circularity > 0.4:  # Reasonably circular
                    # Get center and radius
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    
                    if self.ball_min_radius <= radius <= self.ball_max_radius:
                        confidence = circularity * 0.7 + self._calculate_ball_confidence(frame, int(x), int(y), int(radius)) * 0.3
                        candidates.append((int(x), int(y) + y_offset, confidence, int(radius)))
        
        # Select best candidate
        if candidates:
            # Filter by confidence and select best
            candidates = [c for c in candidates if c[2] > 0.3]  # Minimum confidence threshold
            
            if candidates:
                # Sort by confidence and select best
                best_candidate = max(candidates, key=lambda x: x[2])
                x, y, confidence, radius = best_candidate
                
                return BallDetectionResult(
                    frame_number=frame_number,
                    detected=True,
                    x=float(x),
                    y=float(y),
                    confidence=confidence,
                    bbox=(x-radius, y-radius, x+radius, y+radius)
                )
        
        return BallDetectionResult(frame_number=frame_number, detected=False)
    
    def _detect_ball_in_frame_advanced(self, frame: np.ndarray, frame_number: int, y_offset: int = 0, frame_file: str = "") -> BallDetectionResult:
        """
        Advanced golf ball detection considering shadows and lighting conditions
        CLAUDE.md 7-3: 골프공에 음영이 질 경우를 감안한 로직
        """
        candidates = []
        
        # Method 1: Circle detection using HoughCircles (기본 원형 감지)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Multiple circle detection with different parameters for various lighting conditions
        circle_params = [
            {'param1': 50, 'param2': 30, 'minRadius': self.ball_min_radius, 'maxRadius': self.ball_max_radius},
            {'param1': 40, 'param2': 25, 'minRadius': self.ball_min_radius, 'maxRadius': self.ball_max_radius},
            {'param1': 60, 'param2': 35, 'minRadius': self.ball_min_radius, 'maxRadius': self.ball_max_radius},
        ]
        
        for params in circle_params:
            circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=30,
                **params
            )
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for circle in circles[0, :]:
                    x, y, r = circle
                    confidence = self._calculate_ball_confidence_advanced(frame, x, y, r, frame_number)
                    candidates.append((x, y + y_offset, confidence, r, 'circle'))
        
        # Method 2: Shadow-resistant detection using multiple color spaces
        # CLAUDE.md 7-3: 골프공에 음영이 질 경우 감안
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Enhanced white ball detection in different lighting conditions
        enhanced_masks = []
        
        # HSV-based detection (좀 더 넓은 범위)
        for i, color_range in enumerate(self.ball_color_ranges):
            lower, upper = color_range
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            enhanced_masks.append(('hsv', mask))
        
        # LAB color space for shadow-resistant detection
        # L channel for lightness (음영에 덜 민감)
        l_channel = lab[:, :, 0]
        l_mask = cv2.inRange(l_channel, 120, 255)  # 밝은 영역
        enhanced_masks.append(('lab_l', l_mask))
        
        # Adaptive threshold for varying lighting
        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # Invert to get bright objects
        adaptive_mask = cv2.bitwise_not(adaptive_thresh)
        enhanced_masks.append(('adaptive', adaptive_mask))
        
        # Process each mask
        for mask_type, mask in enhanced_masks:
            # Morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 30 or area > 2000:  # Area constraints
                    continue
                
                # Check if contour is roughly circular
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue
                
                circularity = 4 * math.pi * area / (perimeter * perimeter)
                
                # More lenient circularity for shadow cases
                if circularity > 0.3:  # Reduced threshold for shadows
                    # Get center and radius
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    
                    if self.ball_min_radius <= radius <= self.ball_max_radius:
                        confidence = self._calculate_ball_confidence_advanced(frame, int(x), int(y), int(radius), frame_number)
                        # Boost confidence for certain mask types
                        if mask_type == 'lab_l':
                            confidence *= 1.1  # LAB L-channel is more shadow-resistant
                        elif mask_type == 'adaptive':
                            confidence *= 1.05
                            
                        candidates.append((int(x), int(y) + y_offset, confidence, int(radius), mask_type))
        
        # Select best candidate with advanced filtering
        if candidates:
            # Filter by minimum confidence
            candidates = [c for c in candidates if c[2] > 0.2]  # Lower threshold to catch shadowed balls
            
            if candidates:
                # Sort by confidence and select best
                best_candidate = max(candidates, key=lambda x: x[2])
                x, y, confidence, radius, method = best_candidate
                
                return BallDetectionResult(
                    frame_number=frame_number,
                    detected=True,
                    x=float(x),
                    y=float(y),
                    confidence=confidence,
                    bbox=(x-radius, y-radius, x+radius, y+radius)
                )
        
        return BallDetectionResult(frame_number=frame_number, detected=False)
    
    def _calculate_ball_confidence_advanced(self, frame: np.ndarray, x: int, y: int, radius: int, frame_number: int) -> float:
        """
        Advanced confidence calculation considering shadows and lighting
        """
        height, width = frame.shape[:2]
        
        # Check bounds
        if x < radius or y < radius or x >= width - radius or y >= height - radius:
            return 0.0
        
        confidence = 0.0
        
        # Extract region of interest
        roi = frame[y-radius:y+radius+1, x-radius:x+radius+1]
        
        if roi.size == 0:
            return 0.0
        
        # Multi-color space analysis
        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        roi_lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
        
        # White/light colored regions in HSV
        white_mask = cv2.inRange(roi_hsv, (0, 0, 150), (180, 40, 255))  # More lenient for shadows
        white_ratio = np.sum(white_mask > 0) / white_mask.size
        confidence += white_ratio * 0.3
        
        # Lightness in LAB color space (shadow-resistant)
        l_channel = roi_lab[:, :, 0]
        light_mask = l_channel > 120
        light_ratio = np.sum(light_mask) / light_mask.size
        confidence += light_ratio * 0.3
        
        # Check for circular gradient (typical of spherical objects)
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        center_y, center_x = radius, radius
        
        # Sample intensities at different radii to check for gradient
        gradient_score = 0.0
        if center_y < roi_gray.shape[0] and center_x < roi_gray.shape[1]:
            center_intensity = float(roi_gray[center_y, center_x])
            
            # Check intensities at 1/2 and 3/4 radius
            for r_frac in [0.5, 0.75]:
                sample_r = int(radius * r_frac)
                if sample_r > 0:
                    # Sample at 4 directions
                    samples = []
                    for angle in [0, 90, 180, 270]:
                        dx = int(sample_r * math.cos(math.radians(angle)))
                        dy = int(sample_r * math.sin(math.radians(angle)))
                        sample_x, sample_y = center_x + dx, center_y + dy
                        
                        if 0 <= sample_x < roi_gray.shape[1] and 0 <= sample_y < roi_gray.shape[0]:
                            samples.append(float(roi_gray[sample_y, sample_x]))
                    
                    if samples:
                        avg_intensity = np.mean(samples)
                        # Golf balls typically have brighter centers
                        if center_intensity > avg_intensity:
                            gradient_score += 0.1
        
        confidence += gradient_score
        
        # Green background detection (golf course context)
        sample_radius = min(radius * 2, 40)
        if (x >= sample_radius and y >= sample_radius and 
            x < width - sample_radius and y < height - sample_radius):
            
            background_roi = frame[y-sample_radius:y+sample_radius+1, x-sample_radius:x+sample_radius+1]
            background_hsv = cv2.cvtColor(background_roi, cv2.COLOR_BGR2HSV)
            
            # Green color range for grass (wider range)
            green_mask = cv2.inRange(background_hsv, (25, 30, 30), (95, 255, 255))
            green_ratio = np.sum(green_mask > 0) / green_mask.size
            confidence += green_ratio * 0.2
        
        # Position preference (lower in frame is more likely)
        position_score = (height - y) / height
        confidence += position_score * 0.15
        
        # Size preference
        optimal_radius = 15  # Typical golf ball radius in pixels
        size_score = 1.0 - abs(radius - optimal_radius) / 25
        confidence += max(0, size_score) * 0.05
        
        return min(confidence, 1.0)
    
    def _calculate_ball_confidence(self, frame: np.ndarray, x: int, y: int, radius: int) -> float:
        """
        Calculate confidence score for a potential golf ball
        Considers factors like color, shape, and context
        """
        height, width = frame.shape[:2]
        
        # Check bounds
        if x < radius or y < radius or x >= width - radius or y >= height - radius:
            return 0.0
        
        confidence = 0.0
        
        # Extract region of interest
        roi = frame[y-radius:y+radius+1, x-radius:x+radius+1]
        
        if roi.size == 0:
            return 0.0
        
        # Check color distribution (golf balls are typically white)
        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # White/light colored regions
        white_mask = cv2.inRange(roi_hsv, (0, 0, 180), (180, 30, 255))
        white_ratio = np.sum(white_mask > 0) / white_mask.size
        confidence += white_ratio * 0.4
        
        # Check if it's on green background (golf course)
        # Sample area around the ball
        sample_radius = min(radius * 2, 30)
        if (x >= sample_radius and y >= sample_radius and 
            x < width - sample_radius and y < height - sample_radius):
            
            background_roi = frame[y-sample_radius:y+sample_radius+1, x-sample_radius:x+sample_radius+1]
            background_hsv = cv2.cvtColor(background_roi, cv2.COLOR_BGR2HSV)
            
            # Green color range for grass
            green_mask = cv2.inRange(background_hsv, (35, 50, 50), (85, 255, 255))
            green_ratio = np.sum(green_mask > 0) / green_mask.size
            confidence += green_ratio * 0.3
        
        # Prefer balls in lower part of frame
        position_score = (height - y) / height  # Higher score for lower position
        confidence += position_score * 0.2
        
        # Size preference (medium-sized objects are more likely to be balls)
        size_score = 1.0 - abs(radius - 20) / 30  # Prefer radius around 20 pixels
        confidence += max(0, size_score) * 0.1
        
        return min(confidence, 1.0)
    
    def _identify_hit_moment(self, detections: List[BallDetectionResult]) -> Optional[int]:
        """
        CLAUDE.md Step 8: 골프공이 식별되었다면, 스윙하여 골프공 히팅 순간을 식별함
        8-1) 프레임 별 이미지를 앞 뒤 비교하여 최초 골프공의 픽셀 좌표가 변경된 부분을 찾음
        8-2) 마찬가지로 골프공에 음영 때문에 골프공이 이동한 걸로 오식별 될 수 있으니 이를 감안할 로직이 필요.(기존 골프공과 동일/유사한 색상이 일정 거리 이상 이동했을때만 Hitting 순간으로 파악)
        8-3) 히팅된 순간의 프레임에 대해서는 로깅으로 출력
        """
        logger.info("=" * 50)
        logger.info("CLAUDE.md Step 8: 스윙하여 골프공 히팅 순간 식별")
        logger.info("=" * 50)
        
        # Find consecutive detections
        detected_positions = [(i, d.x, d.y, d.confidence) for i, d in enumerate(detections) if d.detected]
        
        if len(detected_positions) < 3:  # Need at least 3 points for proper analysis
            logger.warning("Step 8: 히팅 순간 식별을 위한 충분한 골프공 감지 결과가 없습니다.")
            logger.warning(f"감지된 위치: {len(detected_positions)}개 (최소 3개 필요)")
            return None
        
        logger.info(f"Step 8-1: {len(detected_positions)}개의 감지된 골프공 위치를 프레임별로 앞뒤 비교하여 분석")
        
        hit_candidates = []  # 히팅 후보 순간들을 저장
        
        # Step 8-1: 프레임별 이미지를 앞뒤 비교하여 최초 골프공의 픽셀 좌표 변경 감지
        for i in range(1, len(detected_positions)):
            prev_frame, prev_x, prev_y, prev_conf = detected_positions[i-1]
            curr_frame, curr_x, curr_y, curr_conf = detected_positions[i]
            
            # Calculate movement distance and direction
            distance = math.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
            
            # Calculate movement vector
            dx = curr_x - prev_x
            dy = curr_y - prev_y
            
            logger.debug(f"Frame {prev_frame}→{curr_frame}: 이동거리={distance:.1f}px, 벡터=({dx:.1f}, {dy:.1f})")
            
            # Step 8-2: 음영으로 인한 오식별 방지 로직
            # 기존 골프공과 동일/유사한 색상이 일정 거리 이상 이동했을때만 Hitting 순간으로 파악
            is_significant_movement = False
            
            if distance > self.min_movement_distance:
                # 신뢰도 기반 검증 (음영으로 인한 신뢰도 저하 고려)
                confidence_threshold = 0.4  # 음영을 고려한 낮은 임계값
                
                if prev_conf >= confidence_threshold and curr_conf >= confidence_threshold:
                    # 연속된 프레임에서의 움직임 패턴 검증
                    if i < len(detected_positions) - 1:
                        next_frame, next_x, next_y, next_conf = detected_positions[i+1]
                        next_distance = math.sqrt((next_x - curr_x)**2 + (next_y - curr_y)**2)
                        
                        # 다음 프레임에서도 계속된 움직임이 있는지 확인
                        if next_distance > self.min_movement_distance / 3:  # 더 관대한 조건
                            # 움직임 방향의 일관성 검사
                            next_dx = next_x - curr_x
                            next_dy = next_y - curr_y
                            
                            # 벡터 내적을 이용한 방향 일관성 검사
                            dot_product = dx * next_dx + dy * next_dy
                            magnitude1 = math.sqrt(dx*dx + dy*dy)
                            magnitude2 = math.sqrt(next_dx*next_dx + next_dy*next_dy)
                            
                            if magnitude1 > 0 and magnitude2 > 0:
                                cos_angle = dot_product / (magnitude1 * magnitude2)
                                angle_degrees = math.degrees(math.acos(max(-1, min(1, cos_angle))))
                                
                                # 방향이 일관성 있으면 (각도가 90도 이하) 유효한 움직임으로 판단
                                if angle_degrees <= 90:
                                    is_significant_movement = True
                                    
                                    logger.info(f"Step 8-2 검증 PASS: Frame {curr_frame}")
                                    logger.info(f"  - 이동거리: {distance:.1f}px")
                                    logger.info(f"  - 신뢰도: {prev_conf:.3f} → {curr_conf:.3f}")
                                    logger.info(f"  - 방향 일관성: {angle_degrees:.1f}°")
                                else:
                                    logger.debug(f"Frame {curr_frame}: 방향 불일치로 제외 ({angle_degrees:.1f}°)")
                            else:
                                is_significant_movement = True  # 벡터 크기가 0인 경우는 허용
                        else:
                            logger.debug(f"Frame {curr_frame}: 후속 움직임이 없어 제외")
                    else:
                        # 마지막 프레임 근처인 경우는 더 관대하게 판단
                        if distance > self.min_movement_distance * 1.5:
                            is_significant_movement = True
                else:
                    logger.debug(f"Frame {curr_frame}: 신뢰도 부족으로 제외 ({prev_conf:.3f}, {curr_conf:.3f})")
            
            if is_significant_movement:
                hit_candidates.append({
                    'frame': curr_frame,
                    'prev_pos': (prev_x, prev_y),
                    'curr_pos': (curr_x, curr_y),
                    'distance': distance,
                    'confidence_avg': (prev_conf + curr_conf) / 2
                })
        
        # 가장 적합한 히팅 순간 선정
        if hit_candidates:
            # 첫 번째 유의미한 움직임을 히팅 순간으로 선정 (시간순)
            hit_moment = hit_candidates[0]
            hit_frame = hit_moment['frame']
            
            # Step 8-3: 히팅된 순간의 프레임에 대해서는 로깅으로 출력
            logger.info("=" * 30)
            logger.info("Step 8-3: 히팅 순간 식별 완료!")
            logger.info("=" * 30)
            logger.info(f"✓ 히팅 프레임: {hit_frame}")
            logger.info(f"✓ 골프공 이동: ({hit_moment['prev_pos'][0]:.1f}, {hit_moment['prev_pos'][1]:.1f}) → ({hit_moment['curr_pos'][0]:.1f}, {hit_moment['curr_pos'][1]:.1f})")
            logger.info(f"✓ 이동 거리: {hit_moment['distance']:.1f} 픽셀")
            logger.info(f"✓ 평균 신뢰도: {hit_moment['confidence_avg']:.3f}")
            logger.info(f"✓ 총 {len(hit_candidates)}개의 히팅 후보 중 첫 번째 선택")
            
            # 추가 후보들도 로깅
            if len(hit_candidates) > 1:
                logger.info("기타 히팅 후보들:")
                for i, candidate in enumerate(hit_candidates[1:], 2):
                    logger.info(f"  {i}번째 후보 - Frame {candidate['frame']}, 거리: {candidate['distance']:.1f}px")
            
            return hit_frame
        
        logger.warning("=" * 30)
        logger.warning("Step 8-3: 히팅 순간을 식별할 수 없습니다")
        logger.warning("=" * 30)
        logger.warning("이유:")
        logger.warning(f"  - 분석된 프레임 쌍: {len(detected_positions)-1}개")
        logger.warning(f"  - 최소 이동 거리: {self.min_movement_distance}px")
        logger.warning(f"  - 유효한 히팅 후보: 0개")
        
        return None
    
    def _track_trajectory(
        self, 
        detections: List[BallDetectionResult], 
        hit_frame: Optional[int],
        total_frames: int
    ) -> List[TrajectoryPoint]:
        """
        CLAUDE.md Step 9: 골프공 이동 경로 탐지
        9-1) 탐지된 골프공 이동경로는 부드럽게 선으로 이어서 표시
        9-2) 골프공이 멀어지면 예측으로 가상 좌표 계산
        """
        trajectory_points = []
        
        # Get detected positions after hit
        if hit_frame is None:
            # If no hit detected, use all detections
            detected_positions = [(i, d.x, d.y, d.confidence) for i, d in enumerate(detections) if d.detected]
        else:
            # Use detections from hit frame onwards
            detected_positions = [(i, d.x, d.y, d.confidence) for i, d in enumerate(detections) 
                                if d.detected and i >= hit_frame]
        
        if len(detected_positions) < 2:
            logger.warning("Not enough trajectory points detected")
            return trajectory_points
        
        # Convert to trajectory points
        for frame_num, x, y, confidence in detected_positions:
            trajectory_points.append(TrajectoryPoint(
                frame_number=frame_num,
                x=x,
                y=y,
                confidence=confidence,
                timestamp=frame_num / 30.0  # Assuming 30 FPS
            ))
        
        # Apply smoothing to trajectory
        trajectory_points = self._smooth_trajectory(trajectory_points)
        
        # Predict trajectory for frames where ball wasn't detected
        if len(trajectory_points) >= 3:
            trajectory_points = self._predict_missing_points(trajectory_points, total_frames)
        
        logger.info(f"Trajectory tracking completed: {len(trajectory_points)} points")
        return trajectory_points
    
    def _smooth_trajectory(self, trajectory_points: List[TrajectoryPoint]) -> List[TrajectoryPoint]:
        """
        Apply smoothing to trajectory points to create smooth trajectory line
        """
        if len(trajectory_points) < 3:
            return trajectory_points
        
        smoothed_points = []
        
        for i, point in enumerate(trajectory_points):
            if i == 0 or i == len(trajectory_points) - 1:
                # Keep first and last points unchanged
                smoothed_points.append(point)
            else:
                # Apply weighted average with neighboring points
                prev_point = trajectory_points[i-1]
                next_point = trajectory_points[i+1]
                
                smoothed_x = (prev_point.x * 0.25 + point.x * 0.5 + next_point.x * 0.25)
                smoothed_y = (prev_point.y * 0.25 + point.y * 0.5 + next_point.y * 0.25)
                
                smoothed_point = TrajectoryPoint(
                    frame_number=point.frame_number,
                    x=smoothed_x,
                    y=smoothed_y,
                    confidence=point.confidence * 0.9,  # Slightly lower confidence for smoothed points
                    timestamp=point.timestamp
                )
                smoothed_points.append(smoothed_point)
        
        return smoothed_points
    
    def _predict_missing_points(
        self, 
        trajectory_points: List[TrajectoryPoint], 
        total_frames: int
    ) -> List[TrajectoryPoint]:
        """
        CLAUDE.md Step 9-2: 골프공이 일정 거리 이상 날라가면 예측으로 궤적을 그림
        """
        if len(trajectory_points) < 3:
            return trajectory_points
        
        # Calculate velocity from last few points
        last_points = trajectory_points[-3:]
        
        # Calculate average velocity
        velocities = []
        for i in range(1, len(last_points)):
            dt = last_points[i].timestamp - last_points[i-1].timestamp
            if dt > 0:
                vx = (last_points[i].x - last_points[i-1].x) / dt
                vy = (last_points[i].y - last_points[i-1].y) / dt
                velocities.append((vx, vy))
        
        if not velocities:
            return trajectory_points
        
        # Average velocity
        avg_vx = sum(v[0] for v in velocities) / len(velocities)
        avg_vy = sum(v[1] for v in velocities) / len(velocities)
        
        # Predict points for remaining frames
        last_point = trajectory_points[-1]
        predicted_points = []
        
        for frame_num in range(last_point.frame_number + 1, min(total_frames, last_point.frame_number + 60)):
            dt = (frame_num - last_point.frame_number) / 30.0
            
            # Apply gravity to vertical velocity (golf ball follows parabolic trajectory)
            gravity = 200  # pixels/second^2 (approximate)
            
            pred_x = last_point.x + avg_vx * dt
            pred_y = last_point.y + avg_vy * dt + 0.5 * gravity * dt * dt
            
            # Reduce confidence for predicted points based on distance from last detection
            confidence = max(0.1, 0.8 - dt * 0.1)
            
            predicted_point = TrajectoryPoint(
                frame_number=frame_num,
                x=pred_x,
                y=pred_y,
                confidence=confidence,
                timestamp=frame_num / 30.0
            )
            predicted_points.append(predicted_point)
            
            # Stop predicting if ball goes too far off screen
            if pred_y > 1000 or pred_x < -100 or pred_x > 2000:
                break
        
        if predicted_points:
            logger.info(f"Predicted {len(predicted_points)} trajectory points")
        
        return trajectory_points + predicted_points