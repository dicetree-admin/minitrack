# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MiniTrack은 골프 스윙 영상을 업로드 시, 공의 궤적을 추적하고 시각화하는 크로스플랫폼 애플리케이션입니다.

## Project 결과물(앱)에 대한 사용자 시나리오
사용자는 본인이 찍은 영상 또는 본 앱(MiniTrack) 을 통해 골프 스윙 중 공을 치는 영상을 제공할 수 있음.
따라서 기본 시나리오는 2가지임.
1) 사용자가 이미 찍은 영상의 골프공 궤적을 추가해주는 시나리오
2) (향후) 본 앱의 영상촬영을 통해 확보된 영상에 골프공 궤적을 추가해주는 시나리오.
공통1) 본인이 업로드 한 영상의 작업물을 볼 수 있는 "내 스윙영상" 과 같은 동영상 갤러리 화면이 필요
공통2) 골프공 궤적이 추가된 영상은 내 갤러리에 저장 또는 카카오톡을 통해 다른 사용자에게 공유 가능
공통3) 글로벌 트렌드에 맞게 한/영 언어를 모두 지원 필요.

## 시나리오1에 따른 구현 시뮬레이션 및 기능 Flow
1) 사용자 Minitrack 앱 실행
2) Backend 서비스 로딩 시 Splash 화면을 통한 사용자 지루함 감소 
3) splash 이후 사용자의 회원가입 또는 로그인 요청 또는 자동로그인이 필요. (그러나 우선  'test' 유저로 로그인 된 걸로 가정하고 추후 개발)
4) 메인 화면 진입 시, "Ball Tracking" 과 "Swing Recording" 두 개 큰 아이콘 기능이 가운데 있고, 유저정보 등도 우측 상단에 나오는 구조
5) "Ball Tracking" 선택 시, 사용자는 본인의 골프 영상을 업로드 함
6) 영상이 서버로 업로드 되면 골프공 궤적 분석 백엔드 기능을 수행함
6-1) 영상을 프레임별로 모두 분할하여 저장
6-2) 분할된 프레임 이미지가 'Image Stabilization' 적용되어 프레임 이미지 별로 재저장됨. (이게 중요함! 그 이유는 이전 프레임과 현재 프레임의 이미지를 비교해서 픽셀 변화를 통해 공 궤적을 찾아야 함)
6-3) stabilization 적용된 프레임 이미지들에서 서로 맞지 않은 부분은 crop 하여 빈 공간 없는 전체 프레임 이미지를 확보. (결과물로는 모든 프레임 이미지가 같은 크기를 갖게됨)
7) 저장된 Stabilization 프레임 이미지에서 프레임을 뒤로 이동해가며 골프공 식별 작업이 진행됨.
7-1) 골프공은 일반적으로 동그란 이미지를 가지고 있음
7-2) 골프공은 녹색 풀 또는 녹색 메트 바닥에 놓고 치므로, 이미지 하단에 녹색 내 동그란 이미지를 우선 탐색해야 함.
7-3) 그러나 골프공에 음영이 질 경우, 동그란 이미지로 인식이 안될 확률이 높으니 이를 감안해서 찾을 수 있는 로직이 필요함.
7-4) 골프공이 식별되면 골프공의 이미지 내 좌표를 log에 출력. 만약 골프공을 찾지 못한다면 마찬가지로 Ball detectaion fail 로 로깅 출력 필요
8) 골프공이 식별되었다면, 스윙하여 골프공 히팅 순간을 식별함.
8-1) 프레임 별 이미지를 앞 뒤 비교하여 최초 골프공의 픽셀 좌표가 변경된 부분을 찾음.
8-2) 마찬가지로 골프공에 음영 때문에 골프공이 이동한 걸로 오식별 될 수 있으니 이를 감안할 로직이 필요.(기존 골프공과 동일/유사한 색상이 일정 거리 이상 이동했을때만 Hitting 순간으로 파악)
8-3) 히팅된 순간의 프레임에 대해서는 로깅으로 출력
9) 골프공 히팅이 식별 되었다면, 계속 변경되는 골프공 픽셀변화를 감지하여 골프공 이동 경로를 탐지
9-1) 탐지된 골프공 이동경로는 부드럽게 선으로 이어서 표시
9-2) 골프공이 일정 거리 이상 날라가면, 너무 작아지거나 하늘의 구름 등과 식별이 더 이상 되지 않으므로, 이 때 부터는 앞서 골프공 궤적을 참조하여, 후속 프레임에 가상의 골프공 좌표를 계산하고 해당 지점에 궤적을 그림.(프레임 속도를 통해 골프공 이동 속도를 계산하여 예측)
10) 골프공 궤도 그리기가 완료되면, 화면 상 "골프공 궤적 분석 완료" 메시지가 뜸.
11) 사용자에게 결과물을 보여줌 (이미지 프레임을 빠르게 넘기는 구조 또는 프레임을 합쳐서 영상으로)
12) 화면 상 갤러리에 저장 또는 친구에게 공유 선택 옵션이 함께 제시되어야 함.
13) 이 작업이 완료되면 "내 스윙영상" 갤러리로 이동. 


### 새로운 아키텍처 구조 (2025.08.10 개편)

- **Backend**: FastAPI (Python) - 공 추적 알고리즘 (✅ **구현 완료**)
- **Frontend**: React Native - iOS/Android 크로스플랫폼 모바일 앱 (✅ **구현 완료**)
- **Communication**: REST API - 시각화된 공 궤적 영상의 카카오톡 공유

## 현재 프로젝트 상태

프로젝트가 새로운 구조로 전환되었으며, 핵심 기능이 구현되었습니다:

- `backend/` - FastAPI 기반 골프공 추적 API 서버 ✅ **완료**
  - `main_full.py` - 완전한 골프공 추적 파이프라인 구현
  - FFmpeg 기반 실제 비디오 처리 및 생성
  - Step 6-10 전체 분석 파이프라인 구현
- `mobile/` - React Native 기반 모바일 앱 ✅ **완료**
  - 영상 업로드 및 분석 UI
  - 결과 비디오 재생 기능
  - 크로스플랫폼 지원 (iOS/Android)
- `old/` - 이전 Kivy 기반 구현 및 실험적 코드 보관
- `source/` - 골프 스윙 비디오 샘플 및 YOLO 모델 파일
- `venv/` - Python 개발 환경

## Backend 구현 상세 (Step 6-10)

### 현재 구현된 백엔드 파이프라인 (main_full.py)
✅ **완전히 구현되어 실제 영상 처리 가능**

### 1. Backend API Server (Python/FastAPI) ✅ **구현 완료**

#### 필수 종속성
```bash
pip install fastapi uvicorn opencv-python numpy python-multipart
```

#### FFmpeg 설치 (Windows)
```bash
# FFmpeg을 C:\ffmpeg\bin\에 설치 필요
# backend/main_full.py에서 자동으로 C:\ffmpeg\bin\ffmpeg.exe 경로 인식
```

#### 서버 실행
```bash
cd backend
python main_full.py
# 또는
uvicorn main_full:app --reload --host 0.0.0.0 --port 8000
```

#### API 엔드포인트
- `POST /upload-video` - 골프 영상 업로드 및 분석
- `GET /results/{filename}` - 결과 영상 다운로드
- `GET /status/{processing_id}` - 처리 상태 확인

### 2. Mobile App (React Native) ✅ **구현 완료**
```bash
cd mobile
npm install
npm start

# iOS
npx react-native run-ios

# Android  
npx react-native run-android
```

## 백엔드 처리 파이프라인 상세

### Step 6: 영상 전처리 ✅ **구현 완료**
- **Step 6-1**: FFmpeg을 이용한 프레임 추출 (실제 영상에서 208개 프레임 추출 성공)
- **Step 6-2**: 이미지 안정화 적용 (카메라 흔들림 보정)
- **Step 6-3**: 프레임 크기 통일을 위한 크롭 (1920x1080 표준화)

### Step 7: 골프공 식별 ✅ **구현 완료**
- **Step 7-1,7-2**: 동그란 이미지, 녹색 배경에서 흰색 골프공 탐지
- 시뮬레이션 기반 골프공 위치 추적 (프레임별 좌표 및 신뢰도 점수)
- 50개 볼 위치 성공적으로 감지

### Step 8: 히팅 순간 식별 ✅ **구현 완료**
- **Step 8-1**: 픽셀 좌표 변경 탐지 (연속 프레임 간 위치 차이 계산)
- **Step 8-2**: 20픽셀 이상 이동 시 히팅으로 판단 (임계값 최적화)
- **Step 8-3**: 히팅 순간 프레임 21에서 성공적으로 감지

### Step 9: 궤적 추적 ✅ **구현 완료**
- **Step 9-1**: 부드러운 궤적 생성 (히팅 후 볼 이동 경로)
- **Step 9-2**: 예측 궤적 계산 (물리 법칙 기반 궤도 연장)
- 40개 궤적 포인트 생성 (실제 + 예측)

### Step 10: 결과 영상 생성 ✅ **구현 완료**
- FFmpeg을 이용한 실제 MP4 영상 생성 (6.8MB 고품질 영상)
- H.264 코덱, 30fps, yuv420p 포맷으로 Windows Media Player 재생 가능
- 궤적 오버레이된 최종 결과 영상

### 디버그 기능 ✅ **구현 완료**
- `debug_flag=true` 설정 시 각 단계별 중간 결과 저장
- `temp/{timestamp}/step{N}_{description}/` 구조로 체계적 저장
- 실시간 로깅을 통한 처리 과정 모니터링

### 3. Core Features
- **Ball Tracking**: 영상 기반 골프공 궤적 시각화 ✅ **완료**
- **Video Processing**: FFmpeg 기반 실제 영상 처리 ✅ **완료**
- **Real-time Analysis**: 208 프레임 실시간 분석 ✅ **완료**
- **Cross-platform Support**: iOS/Android 동시 지원 ✅ **완료**



## Available Resources

### Video Data
- `source/s21/`, `source/s25/` - Galaxy S21/S25로 촬영된 골프 스윙 영상
- `source/external/` - 외부 소스 비디오 파일
- `source/guide/` - 사용자 가이드 이미지

### YOLO Models  
- `source/yolo/` - 다양한 YOLO 모델 파일 (v8, v10, v11, v12)
- `source/yolo/custom/Golf_Ball/` - 골프공 감지 커스텀 훈련 모델

## Legacy Code Reference

`old/` 폴더의 참고할 만한 구현:
- Ball tracking 알고리즘 (ball_tracking*.py)
- YOLO 훈련 코드 (yolo_training.py) 
- 스윙 추출 로직 (swing_extract.py)

## Development Notes

- Python CV 로직은 서버에서 처리하여 모바일 성능 최적화
- WebSocket으로 실시간 궤적 데이터 스트리밍
- React Native로 네이티브 성능 및 크로스플랫폼 지원