import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const SplashContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
  color: white;
  text-align: center;
  padding: 20px;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
`;

const Subtitle = styled.h2`
  font-size: 1.2rem;
  color: #E8F5E8;
  margin-bottom: 2rem;
  font-weight: 600;
`;

const Description = styled.p`
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 3rem;
  max-width: 500px;
`;

const LoadingSpinner = styled.div`
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const LoadingText = styled.p`
  font-size: 1rem;
  font-weight: 500;
`;

const SplashScreen: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // CLAUDE.md Step 1-2: Backend 서비스 로딩 시 Splash 화면을 통한 사용자 지루함 감소
    const initializeApp = async () => {
      try {
        console.log('Step 1: MiniTrack 앱 실행');
        console.log('Step 2: Backend 서비스 로딩 시작');
        
        // Progressive loading steps with user feedback
        const loadingSteps = [
          { message: 'Initializing services...', duration: 800 },
          { message: 'Connecting to server...', duration: 1000 },
          { message: 'Loading vision models...', duration: 1200 },
          { message: 'Preparing tracking engine...', duration: 1000 },
        ];
        
        for (const step of loadingSteps) {
          console.log(`Backend Loading: ${step.message}`);
          await new Promise(resolve => setTimeout(resolve, step.duration));
        }
        
        // Check backend connectivity
        console.log('Checking backend connectivity...');
        try {
          const response = await fetch('http://localhost:8000/', {
            signal: AbortSignal.timeout(5000)
          });
          
          if (response.ok) {
            console.log('Backend service connected successfully');
          } else {
            console.warn('Backend service responded with error:', response.status);
          }
        } catch (error) {
          console.warn('Backend connection failed, running in offline mode:', error);
        }
        
        // CLAUDE.md Step 3: 우선 'test' 유저로 로그인 된 걸로 가정하고 추후 개발
        console.log('Step 3: Auto-login as test user (임시 구현)');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        console.log('앱 초기화 완료, 메인 화면으로 이동');
        navigate('/main');
        
      } catch (error) {
        console.error('앱 초기화 실패:', error);
        // Continue to main screen even if initialization fails
        navigate('/main');
      }
    };

    initializeApp();
  }, [navigate]);

  return (
    <SplashContainer>
      <Title>MiniTrack</Title>
      <Subtitle>Golf Ball Trajectory Tracker</Subtitle>
      <Description>
        골프 스윙 영상을 분석하여 공의 궤적을 시각화하는 스마트 분석 도구입니다.
      </Description>
      
      <LoadingSpinner />
      <LoadingText>서비스 로딩 중...</LoadingText>
    </SplashContainer>
  );
};

export default SplashScreen;