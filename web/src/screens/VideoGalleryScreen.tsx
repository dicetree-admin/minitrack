import React from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
// Using emoji icons for simplicity

const Container = styled.div`
  min-height: 100vh;
  background: #F5F5F5;
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
`;

const BackButton = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  
  &:hover {
    background: rgba(46, 125, 50, 0.1);
  }
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
`;

const EmptyState = styled.div`
  background: white;
  border-radius: 16px;
  padding: 60px 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const EmptyIcon = styled.div`
  margin-bottom: 16px;
`;

const EmptyTitle = styled.h2`
  font-size: 20px;
  font-weight: bold;
  color: #666;
  margin: 0 0 8px 0;
`;

const EmptyDescription = styled.p`
  font-size: 16px;
  color: #999;
  margin: 0 0 24px 0;
  line-height: 1.5;
`;

const StartButton = styled.button`
  background: #2E7D32;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px 32px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s ease;

  &:hover {
    background: #1B5E20;
  }
`;

const VideoGalleryScreen: React.FC = () => {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/main');
  };

  const handleStartTracking = () => {
    navigate('/ball-tracking');
  };

  return (
    <Container>
      <Header>
        <BackButton onClick={handleBack}>
          <span style={{fontSize: '24px', color: '#2E7D32'}}>←</span>
        </BackButton>
        <Title>내 스윙영상</Title>
      </Header>

      {/* Empty state - 실제로는 저장된 영상들이 리스트로 표시됨 */}
      <EmptyState>
        <EmptyIcon>
          <span style={{fontSize: '64px', color: '#CCC'}}>📁</span>
        </EmptyIcon>
        <EmptyTitle>아직 분석된 영상이 없습니다</EmptyTitle>
        <EmptyDescription>
          골프 스윙 영상을 업로드하고 궤적 분석을 시작해보세요.<br/>
          분석이 완료된 영상들이 여기에 저장됩니다.
        </EmptyDescription>
        <StartButton onClick={handleStartTracking}>
          첫 번째 영상 분석하기
        </StartButton>
      </EmptyState>
    </Container>
  );
};

export default VideoGalleryScreen;