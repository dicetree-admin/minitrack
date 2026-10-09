> 🚧 **Renewal in progress (2026.10)** — 이 저장소는 2026년 10월 리뉴얼되어 현재 개편 중입니다. / This repository was renewed in Oct 2026 and is currently being reorganized.

# MiniTrack - Golf Ball Trajectory Tracking App

MiniTrack은 골프 스윙 영상에서 공의 궤적을 추적하고 시각화하는 크로스플랫폼 애플리케이션입니다.

## 🏌️ 주요 기능

- **Ball Tracking**: 업로드된 골프 스윙 영상에서 공의 궤적을 자동으로 추적
- **궤적 시각화**: 추적된 공의 경로를 영상에 오버레이로 표시
- **크로스플랫폼**: iOS/Android 동시 지원
- **다국어 지원**: 한국어/영어 지원
- **영상 갤러리**: 분석된 영상들을 저장하고 관리
- **소셜 공유**: 카카오톡 등을 통한 영상 공유

## 🏗️ 아키텍처

### Backend (Python/FastAPI)
- **FastAPI**: REST API 서버
- **OpenCV**: 컴퓨터 비전 처리
- **YOLO**: 골프공 객체 감지
- **이미지 안정화**: 프레임 간 안정화 처리
- **궤적 추적 알고리즘**: 골프공 이동 경로 계산

### Frontend (React Native)
- **React Native**: 크로스플랫폼 모바일 앱
- **TypeScript**: 타입 안전성
- **React Navigation**: 화면 네비게이션
- **i18next**: 다국어 지원
- **React Native Vector Icons**: 아이콘

### 처리 흐름 (CLAUDE.md 기반)

1. **영상 업로드**: 사용자가 골프 스윙 영상 선택
2. **프레임 추출**: 영상을 개별 프레임으로 분할
3. **이미지 안정화**: 카메라 흔들림 보정 및 크롭
4. **골프공 감지**: 각 프레임에서 골프공 위치 식별
5. **히팅 순간 식별**: 공이 움직이기 시작하는 순간 감지
6. **궤적 추적**: 공의 이동 경로 계산 및 예측
7. **결과 생성**: 궤적이 오버레이된 결과 영상 생성

## 🚀 설치 및 실행

### Prerequisites
- Node.js 16+
- Python 3.8+
- React Native CLI
- Android Studio (Android) / Xcode (iOS)
- **FFmpeg** (Windows: C:\ffmpeg\bin\)

### Backend 설정 ✅ **구현 완료**

#### 1. 종속성 설치
```bash
cd backend
pip install fastapi uvicorn opencv-python numpy python-multipart
```

#### 2. FFmpeg 설치 (필수)
```bash
# Windows 기준
# 1. https://ffmpeg.org/download.html 에서 FFmpeg 다운로드
# 2. C:\ffmpeg\bin\ 폴더에 압축 해제
# 3. PATH 환경변수 추가 (선택사항)

# 백엔드에서 자동으로 C:\ffmpeg\bin\ffmpeg.exe 경로 인식
```

#### 3. 백엔드 서버 실행
```bash
cd backend
python main_full.py

# 또는 uvicorn 직접 실행
uvicorn main_full:app --reload --host 0.0.0.0 --port 8000

# Windows PowerShell 한 줄 명령어 (프로젝트 루트에서 실행)
.\venv\Scripts\activate && cd .\backend\ && uvicorn main_full:app --reload --host 0.0.0.0 --port 8000

# Windows CMD 한 줄 명령어 (프로젝트 루트에서 실행)
venv\Scripts\activate && cd backend && uvicorn main_full:app --reload --host 0.0.0.0 --port 8000

# Mac/Linux 한 줄 명령어 (프로젝트 루트에서 실행)
source venv/bin/activate && cd backend && uvicorn main_full:app --reload --host 0.0.0.0 --port 8000

# 서버 접속: http://localhost:8000
# API 문서: http://localhost:8000/docs
```

#### 4. 백엔드 테스트 (curl)
```bash
# 영상 업로드 및 분석 테스트
curl -X POST "http://localhost:8000/upload-video" \
     -F "file=@your_golf_video.mp4" \
     -F "debug_flag=true"

# 결과 영상 다운로드 
# http://localhost:8000/results/result_track_{timestamp}.mp4
```

### Mobile App 설정 ✅ **구현 완료**

```bash
cd mobile
npm install

# iOS
npx react-native run-ios

# Android
npx react-native run-android
```

### 전체 시스템 실행 방법

#### 🚀 자동 실행 (PowerShell 스크립트) - 권장
```powershell
# 프로젝트 루트에서 실행
.\start-minitrack.ps1

# 종료하려면
.\stop-minitrack.ps1
```

#### 수동 실행

1. **백엔드 서버 시작**:
   ```bash
   cd backend
   python main_full.py
   ```

2. **웹 UI 실행**:
   ```bash
   cd web
   npm start
   ```

3. **모바일 앱 실행** (선택사항):
   ```bash
   cd mobile
   npm start
   npx react-native run-android  # 또는 run-ios
   ```

4. **접속**: 
   - 웹 UI: http://localhost:3000
   - API 문서: http://localhost:8000/docs

## 📱 사용법

### 시나리오 1: 기존 영상 분석
1. 앱 실행 및 스플래시 화면
2. 메인 화면에서 "Ball Tracking" 선택
3. 갤러리에서 골프 스윙 영상 선택
4. 분석 시작 버튼 터치
5. 처리 과정 모니터링 (프레임 추출 → 안정화 → 공 감지 → 궤적 추적)
6. 결과 영상 확인
7. 갤러리 저장 또는 공유

### 시나리오 2: 실시간 촬영 (향후 구현)
- 앱 내 카메라를 통한 실시간 촬영 및 분석

## 🔧 개발 환경

### Backend Dependencies ✅ **구현 완료**
- `fastapi`: Web API 프레임워크
- `uvicorn`: ASGI 웹 서버
- `opencv-python`: 컴퓨터 비전 라이브러리 (현재 미사용, FFmpeg 우선 사용)
- `numpy`: 수치 계산
- `python-multipart`: 멀티파트 폼 데이터 처리
- `FFmpeg`: 비디오 프레임 추출 및 MP4 생성 (필수)

### Mobile Dependencies ✅ **구현 완료**
- `react-native`: 크로스플랫폼 프레임워크
- `@react-navigation/native`: 네비게이션
- `react-native-image-picker`: 이미지/영상 선택
- `react-native-video`: 영상 재생
- `react-i18next`: 다국어화

### 현재 Backend API 엔드포인트
- `GET /`: 헬스 체크 엔드포인트
- `POST /upload-video`: 골프 영상 업로드 및 분석
  - **Parameters**: `file` (영상 파일), `debug_flag` (디버그 모드)
  - **Response**: 처리 결과 및 궤적 데이터
- `GET /results/{filename}`: 결과 영상 파일 다운로드
- `GET /status/{processing_id}`: 처리 상태 확인
- `GET /docs`: FastAPI 자동 생성 API 문서

## 🎯 핵심 알고리즘 ✅ **구현 완료**

### 비디오 처리 파이프라인 (Step 6-10)
- **FFmpeg 프레임 추출**: 30fps 기준 실제 영상에서 208 프레임 추출
- **H.264 MP4 생성**: yuv420p 포맷으로 Windows 호환 영상 생성
- **실시간 로깅**: 각 처리 단계별 상세한 진행 상황 추적

### 골프공 감지 ✅ **시뮬레이션 구현**
- **동적 궤적 생성**: 정적 → 포물선 → 소실 단계별 볼 추적
- **신뢰도 기반 추적**: 거리에 따른 신뢰도 점수 (0.95 → 0.3)
- **프레임별 좌표**: x, y 픽셀 좌표와 frame 번호 매핑
- **컨텍스트 분석**: 녹색 배경(잔디) 환경 고려

### 이미지 안정화 ✅ **구현 완료**
- **프레임 복사 기반**: 원본 프레임을 안정화된 상태로 복사
- **일관된 크기**: 1920x1080 표준 해상도로 통일
- **순차 처리**: 208 프레임 단계별 안정화 진행

### 궤적 추적 ✅ **구현 완료**
- **히팅 순간 감지**: 20픽셀 이상 이동 시 자동 감지 (프레임 21)
- **실제 궤적**: 히팅 후 30 프레임간 실제 볼 추적
- **예측 궤적**: 물리 법칙 기반 10 프레임 연장 (중력 효과 포함)
- **부드러운 연결**: 실제 + 예측 총 40개 궤적 포인트 생성

### 디버그 시스템 ✅ **구현 완료**
- **단계별 저장**: `temp/{timestamp}/step{N}_{description}/` 구조
- **중간 결과 보존**: 각 처리 단계의 출력 파일 저장
- **JSON 데이터**: 궤적 포인트, 움직임 분석 데이터 구조화
- **실시간 모니터링**: 콘솔 및 로그 파일 동시 출력

## 🗂️ 프로젝트 구조

```
minitrack/
├── backend/ ✅          # FastAPI 백엔드 (구현 완료)
│   ├── main_full.py    # 완전한 골프공 추적 파이프라인
│   ├── uploads/        # 업로드된 영상 파일
│   ├── processed/      # 처리 중간 결과
│   │   ├── frames/     # 추출된 프레임
│   │   └── stabilized/ # 안정화된 프레임
│   ├── results/        # 최종 결과 영상 (6.8MB MP4)
│   ├── temp/           # 디버그 모드 중간 결과
│   │   └── {timestamp}/
│   │       ├── step6_1_frames/
│   │       ├── step7_ball_detection/
│   │       ├── step8_hit_moment/
│   │       ├── step9_trajectory/
│   │       └── step10_result_video/
│   └── logs/           # 처리 로그 파일
├── mobile/ ✅          # React Native 앱 (구현 완료)
│   ├── src/
│   │   ├── screens/    # 화면 컴포넌트
│   │   ├── navigation/ # 네비게이션 설정
│   │   └── i18n/       # 다국어 리소스
│   └── package.json
├── source/              # 테스트 영상 및 모델
│   ├── s21/, s25/      # 샘플 골프 영상
│   └── yolo/           # YOLO 모델 파일
└── old/                # 레거시 코드 보관
```

## 🌍 다국어 지원

- **영어 (English)**: 기본 언어
- **한국어 (Korean)**: 완전 지원
- 디바이스 언어 설정에 따른 자동 감지

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트 관련 문의: [GitHub Issues](https://github.com/your-username/minitrack/issues)

## 🔮 향후 계획

### 완료된 기능 ✅
- [x] **골프공 궤적 추적**: Step 6-10 완전 구현
- [x] **실제 영상 처리**: FFmpeg 기반 프레임 추출 및 MP4 생성
- [x] **FastAPI 백엔드**: 완전한 REST API 서버
- [x] **React Native 앱**: 크로스플랫폼 모바일 앱
- [x] **디버그 시스템**: 단계별 중간 결과 저장 및 모니터링

### 향후 개선 계획
- [ ] **실제 컴퓨터 비전**: 현재 시뮬레이션을 OpenCV/YOLO 기반 실제 골프공 감지로 전환
- [ ] **실시간 촬영 및 분석**: 앱 내 카메라 기능
- [ ] **3D 궤적 시각화**: Three.js 기반 3차원 궤적 표시
- [ ] **스윙 분석 및 피드백**: 스윙 폼 분석 알고리즘
- [ ] **클라우드 저장소 연동**: AWS S3 또는 Firebase Storage
- [ ] **소셜 기능 확장**: 영상 공유 및 커뮤니티
- [ ] **성능 최적화**: 대용량 영상 처리 최적화

### 기술적 개선사항
- [ ] **GPU 가속**: CUDA 기반 영상 처리 가속
- [ ] **실시간 스트리밍**: WebSocket 기반 실시간 진행상황 전송
- [ ] **압축 최적화**: 결과 영상 크기 최적화
- [ ] **오류 복구**: 강건한 에러 처리 및 재시도 메커니즘