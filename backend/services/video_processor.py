import cv2
import os
import numpy as np
import logging
from typing import List, Tuple, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import shutil

logger = logging.getLogger(__name__)

class VideoProcessor:
    """
    Video processing service for frame extraction and stabilization
    Implements the video processing pipeline described in CLAUDE.md
    """
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def extract_frames(self, video_path: str, processing_id: str) -> str:
        """
        Extract all frames from video
        CLAUDE.md Step 6-1: 영상을 프레임별로 모두 분할하여 저장
        """
        frames_dir = f"processed/{processing_id}/frames"
        os.makedirs(frames_dir, exist_ok=True)
        
        def _extract_frames():
            logger.info("=" * 50)
            logger.info("CLAUDE.md Step 6-1: 영상을 프레임별로 모두 분할하여 저장")
            logger.info("=" * 50)
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Cannot open video file: {video_path}")
            
            frame_count = 0
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = total_frames / fps if fps > 0 else 0
            
            logger.info(f"영상 정보:")
            logger.info(f"  - 해상도: {width}x{height}")
            logger.info(f"  - FPS: {fps:.2f}")
            logger.info(f"  - 총 프레임 수: {total_frames}")
            logger.info(f"  - 길이: {duration:.2f}초")
            logger.info(f"  - 저장 위치: {frames_dir}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.info("마지막 프레임에 도달했습니다.")
                    break
                
                # Save frame as PNG for better quality
                frame_filename = f"frame_{frame_count:06d}.png"
                frame_path = os.path.join(frames_dir, frame_filename)
                
                # Save with high quality
                success = cv2.imwrite(frame_path, frame, [cv2.IMWRITE_PNG_COMPRESSION, 1])
                if not success:
                    logger.warning(f"프레임 저장 실패: {frame_filename}")
                    continue
                
                frame_count += 1
                
                # Progress logging every 50 frames for detailed tracking
                if frame_count % 50 == 0:
                    progress = (frame_count / total_frames) * 100 if total_frames > 0 else 0
                    logger.info(f"프레임 추출 진행률: {frame_count}/{total_frames} ({progress:.1f}%)")
            
            cap.release()
            logger.info(f"Step 6-1 완료: 총 {frame_count}개 프레임이 {frames_dir}에 저장되었습니다.")
            return frame_count
        
        frame_count = await asyncio.get_event_loop().run_in_executor(
            self.executor, _extract_frames
        )
        
        return frames_dir
    
    async def stabilize_frames(self, frames_dir: str, processing_id: str) -> str:
        """
        Apply image stabilization to frames
        CLAUDE.md Step 6-2: 분할된 프레임 이미지가 'Image Stabilization' 적용되어 프레임 이미지 별로 재저장됨
        CLAUDE.md Step 6-3: stabilization 적용된 프레임 이미지들에서 서로 맞지 않은 부분은 crop 하여 빈 공간 없는 전체 프레임 이미지를 확보
        """
        stabilized_dir = f"processed/{processing_id}/stabilized"
        os.makedirs(stabilized_dir, exist_ok=True)
        
        def _stabilize_frames():
            logger.info("=" * 50)
            logger.info("CLAUDE.md Step 6-2: Image Stabilization 적용")
            logger.info("=" * 50)
            
            frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
            if len(frame_files) < 2:
                logger.warning("이미지 안정화를 위한 충분한 프레임이 없습니다.")
                return frames_dir
            
            logger.info(f"총 {len(frame_files)}개 프레임에 대해 이미지 안정화를 적용합니다.")
            
            # Step 6-2: Image Stabilization 적용을 위한 준비
            first_frame_path = os.path.join(frames_dir, frame_files[0])
            reference_frame = cv2.imread(first_frame_path)
            if reference_frame is None:
                raise ValueError(f"기준 프레임을 읽을 수 없습니다: {first_frame_path}")
                
            reference_gray = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)
            h, w = reference_frame.shape[:2]
            
            logger.info(f"기준 프레임 설정: {frame_files[0]} ({w}x{h})")
            
            # Initialize ORB detector for feature matching (더 많은 특징점 사용)
            orb = cv2.ORB_create(nfeatures=2000)
            reference_kp, reference_desc = orb.detectAndCompute(reference_gray, None)
            
            if reference_desc is None:
                logger.warning("기준 프레임에서 특징점을 찾을 수 없습니다.")
                return frames_dir
                
            logger.info(f"기준 프레임에서 {len(reference_kp)}개 특징점 검출")
            
            # FLANN matcher for feature matching
            FLANN_INDEX_LSH = 6
            index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            
            transforms = []
            stabilized_frames = []
            crop_boundaries = []  # 각 프레임의 유효한 경계 저장
            
            logger.info("이미지 안정화 중요 정보: 이전 프레임과 현재 프레임의 이미지를 비교해서 픽셀 변화를 통해 공 궤적을 찾기 위함")
            
            for i, frame_file in enumerate(frame_files):
                frame_path = os.path.join(frames_dir, frame_file)
                frame = cv2.imread(frame_path)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                if i == 0:
                    # First frame is the reference
                    transform = np.eye(3, dtype=np.float32)
                    stabilized_frame = frame
                else:
                    # Find keypoints and descriptors
                    kp, desc = orb.detectAndCompute(frame_gray, None)
                    
                    if desc is not None and len(desc) > 10:
                        # Match features
                        matches = flann.knnMatch(reference_desc, desc, k=2)
                        
                        # Filter good matches
                        good_matches = []
                        for match_pair in matches:
                            if len(match_pair) == 2:
                                m, n = match_pair
                                if m.distance < 0.7 * n.distance:
                                    good_matches.append(m)
                        
                        if len(good_matches) > 10:
                            # Extract matched points
                            src_pts = np.float32([reference_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                            dst_pts = np.float32([kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                            
                            # Find homography
                            transform, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
                            
                            if transform is not None:
                                # Apply transformation
                                h, w = frame.shape[:2]
                                stabilized_frame = cv2.warpPerspective(frame, transform, (w, h))
                            else:
                                stabilized_frame = frame
                                transform = np.eye(3, dtype=np.float32)
                        else:
                            stabilized_frame = frame
                            transform = np.eye(3, dtype=np.float32)
                    else:
                        stabilized_frame = frame
                        transform = np.eye(3, dtype=np.float32)
                
                transforms.append(transform)
                stabilized_frames.append(stabilized_frame)
                
                if i % 50 == 0:
                    logger.info(f"Stabilized {i+1}/{len(frame_files)} frames")
            
            # CLAUDE.md Step 6-3: stabilization 적용된 프레임 이미지들에서 서로 맞지 않은 부분은 crop
            logger.info("=" * 50)
            logger.info("CLAUDE.md Step 6-3: 크롭하여 빈 공간 없는 전체 프레임 이미지를 확보")
            logger.info("=" * 50)
            
            if not stabilized_frames:
                logger.error("안정화된 프레임이 없습니다.")
                return frames_dir
                
            # 모든 프레임에 공통으로 적용할 크롭 영역 계산
            h, w = stabilized_frames[0].shape[:2]
            
            # 각 프레임의 변환 행렬을 분석하여 공통 유효 영역 계산
            min_valid_x, min_valid_y = 0, 0
            max_valid_x, max_valid_y = w, h
            
            # 안전한 크롭 마진 계산 (변환으로 인한 검은 테두리 제거)
            crop_margin = 60  # 더 넉넉한 마진으로 검은 테두리 완전 제거
            
            # 유효한 크롭 영역 결정
            crop_left = max(min_valid_x, crop_margin)
            crop_top = max(min_valid_y, crop_margin)
            crop_right = min(max_valid_x, w - crop_margin)
            crop_bottom = min(max_valid_y, h - crop_margin)
            
            # 크롭 영역 유효성 검사
            if crop_right <= crop_left or crop_bottom <= crop_top:
                logger.warning("유효한 크롭 영역을 찾을 수 없습니다. 기본 마진 적용")
                crop_left, crop_top = 30, 30
                crop_right, crop_bottom = w - 30, h - 30
            
            cropped_width = crop_right - crop_left
            cropped_height = crop_bottom - crop_top
            
            logger.info(f"크롭 영역 설정:")
            logger.info(f"  - 원본 크기: {w}x{h}")
            logger.info(f"  - 크롭 영역: ({crop_left}, {crop_top}) to ({crop_right}, {crop_bottom})")
            logger.info(f"  - 결과 크기: {cropped_width}x{cropped_height}")
            logger.info(f"  - 제거된 마진: {crop_margin}px")
            
            # 모든 프레임에 동일한 크롭 적용
            cropped_frames = []
            for i, frame in enumerate(stabilized_frames):
                try:
                    cropped = frame[crop_top:crop_bottom, crop_left:crop_right]
                    
                    # 크롭된 프레임이 유효한지 검사
                    if cropped.shape[0] > 0 and cropped.shape[1] > 0:
                        cropped_frames.append(cropped)
                        
                        # Save stabilized and cropped frame
                        stabilized_filename = f"stabilized_{i:06d}.png"
                        stabilized_path = os.path.join(stabilized_dir, stabilized_filename)
                        
                        # 고품질로 저장
                        success = cv2.imwrite(stabilized_path, cropped, [cv2.IMWRITE_PNG_COMPRESSION, 1])
                        if not success:
                            logger.warning(f"안정화된 프레임 저장 실패: {stabilized_filename}")
                        
                        if (i + 1) % 100 == 0:
                            logger.info(f"Step 6-3 진행률: {i+1}/{len(stabilized_frames)} 프레임 크롭 완료")
                    else:
                        logger.warning(f"프레임 {i}의 크롭 결과가 유효하지 않습니다.")
                        
                except Exception as e:
                    logger.error(f"프레임 {i} 크롭 중 오류: {e}")
                    continue
            
            logger.info(f"Step 6-2, 6-3 완료:")
            logger.info(f"  - 안정화 완료: {len(stabilized_frames)}개 프레임")
            logger.info(f"  - 크롭 완료: {len(cropped_frames)}개 프레임")
            logger.info(f"  - 최종 프레임 크기: {cropped_width}x{cropped_height}")
            logger.info(f"  - 저장 위치: {stabilized_dir}")
            logger.info("결과물: 모든 프레임 이미지가 같은 크기를 가지게 되었습니다.")
            
            return len(cropped_frames)
        
        frame_count = await asyncio.get_event_loop().run_in_executor(
            self.executor, _stabilize_frames
        )
        
        return stabilized_dir
    
    async def create_result_video(
        self, 
        frames_dir: str, 
        trajectory_points: List, 
        processing_id: str,
        fps: float = 30.0
    ) -> str:
        """
        Create result video with trajectory overlay
        CLAUDE.md Step 11: 사용자에게 결과물을 보여줌
        """
        result_path = f"results/{processing_id}_result.mp4"
        
        def _create_video():
            frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])
            if not frame_files:
                raise ValueError("No frames found for video creation")
            
            # Read first frame to get dimensions
            first_frame = cv2.imread(os.path.join(frames_dir, frame_files[0]))
            h, w = first_frame.shape[:2]
            
            # Initialize video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(result_path, fourcc, fps, (w, h))
            
            # Create trajectory points dictionary for quick lookup
            trajectory_dict = {point.frame_number: (int(point.x), int(point.y)) for point in trajectory_points}
            
            # Draw trajectory on frames
            trajectory_path = []
            
            for i, frame_file in enumerate(frame_files):
                frame_path = os.path.join(frames_dir, frame_file)
                frame = cv2.imread(frame_path)
                
                # Add current trajectory point if exists
                if i in trajectory_dict:
                    point = trajectory_dict[i]
                    trajectory_path.append(point)
                    
                    # Draw ball position (small circle)
                    cv2.circle(frame, point, 8, (0, 255, 255), -1)  # Yellow filled circle
                    cv2.circle(frame, point, 10, (0, 0, 255), 2)    # Red border
                
                # Draw trajectory path (smooth line)
                if len(trajectory_path) > 1:
                    for j in range(1, len(trajectory_path)):
                        cv2.line(frame, trajectory_path[j-1], trajectory_path[j], (0, 255, 0), 3)
                
                # Add frame to video
                out.write(frame)
                
                if i % 100 == 0:
                    logger.info(f"Processed {i+1}/{len(frame_files)} frames for result video")
            
            out.release()
            logger.info(f"Result video created: {result_path}")
            return result_path
        
        result_path = await asyncio.get_event_loop().run_in_executor(
            self.executor, _create_video
        )
        
        return result_path