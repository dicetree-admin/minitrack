import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styled from 'styled-components';
// Using emoji icons for simplicity

const Container = styled.div`
  min-height: 100vh;
  background: #F5F5F5;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
`;

const SuccessBanner = styled.div`
  background: #E8F5E8;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  margin-bottom: 20px;
  border: 1px solid #C8E6C9;
`;

const SuccessTitle = styled.h2`
  font-size: 20px;
  font-weight: bold;
  color: #2E7D32;
  margin: 8px 0 4px 0;
`;

const SuccessDescription = styled.p`
  font-size: 14px;
  color: #4CAF50;
  margin: 0;
`;

const VideoContainer = styled.div`
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
  aspect-ratio: 16/9;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const VideoPlaceholder = styled.div`
  color: white;
  text-align: center;
  padding: 40px;
`;

const VideoText = styled.p`
  margin: 10px 0 0 0;
  font-size: 14px;
  opacity: 0.8;
`;

const InfoContainer = styled.div`
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const InfoTitle = styled.h3`
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
`;

const InfoRow = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
`;

const InfoLabel = styled.span`
  font-size: 14px;
  color: #666;
  margin-left: 8px;
  flex: 1;
`;

const InfoValue = styled.span`
  font-size: 14px;
  font-weight: 600;
  color: #333;
`;

const ActionContainer = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
`;

const ActionButton = styled.button`
  flex: 1;
  border: none;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-1px);
  }
`;

const SaveButton = styled(ActionButton)`
  background: #4CAF50;
  color: white;
`;

const ShareButton = styled(ActionButton)`
  background: #2196F3;
  color: white;
`;

const GalleryButton = styled.button`
  background: white;
  border: none;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-1px);
  }
`;

const GalleryButtonLeft = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

const GalleryButtonText = styled.span`
  font-size: 16px;
  font-weight: 600;
  color: #2E7D32;
`;

const TipsContainer = styled.div`
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const TipsTitle = styled.h3`
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
`;

const TipItem = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
`;

const TipText = styled.span`
  font-size: 14px;
  color: #666;
  flex: 1;
  line-height: 1.4;
`;

const ResultScreen: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get data passed from BallTrackingScreen
  const { processingId, videoUrl, originalVideo } = location.state || {
    processingId: 'demo-result',
    videoUrl: '/demo-result.mp4',
    originalVideo: null
  };

  const handleSaveToGallery = async () => {
    // CLAUDE.md Step 12: 갤러리에 저장 옵션
    try {
      // In a real implementation, this would save to device storage
      alert('갤러리에 저장되었습니다!');
    } catch (error) {
      alert('저장 중 오류가 발생했습니다.');
    }
  };

  const handleShare = async () => {
    // CLAUDE.md Step 12: 친구에게 공유 선택 옵션 (카카오톡 공유)
    try {
      if (navigator.share) {
        await navigator.share({
          title: 'Golf Ball Trajectory Analysis',
          text: 'MiniTrack으로 분석한 골프 스윙 궤적을 확인해보세요!',
          url: window.location.href
        });
      } else {
        // Fallback for browsers that don't support Web Share API
        const shareUrl = `https://wa.me/?text=${encodeURIComponent('MiniTrack으로 분석한 골프 스윙 궤적을 확인해보세요! ' + window.location.href)}`;
        window.open(shareUrl, '_blank');
      }
    } catch (error) {
      console.log('Share cancelled or failed:', error);
    }
  };

  const handleGoToGallery = () => {
    // CLAUDE.md Step 13: "내 스윙영상" 갤러리로 이동
    navigate('/gallery');
  };

  return (
    <Container>
      {/* Success Message */}
      <SuccessBanner>
        <span style={{fontSize: '32px', color: '#4CAF50'}}>✅</span>
        <SuccessTitle>
          골프공 궤적 분석 완료!
        </SuccessTitle>
        <SuccessDescription>
          공의 궤적이 성공적으로 추가되었습니다.
        </SuccessDescription>
      </SuccessBanner>

      {/* Video Player Placeholder */}
      <VideoContainer>
        <VideoPlaceholder>
          <span style={{fontSize: '64px', color: '#4CAF50'}}>✅</span>
          <VideoText>궤적이 추가된 결과 영상</VideoText>
          <VideoText>실제 구현 시 여기에 결과 영상이 재생됩니다</VideoText>
        </VideoPlaceholder>
      </VideoContainer>

      {/* Analysis Information */}
      <InfoContainer>
        <InfoTitle>분석 정보</InfoTitle>
        
        <InfoRow>
          <span style={{fontSize: '20px', color: '#2E7D32'}}>✓</span>
          <InfoLabel>처리 ID:</InfoLabel>
          <InfoValue>{processingId}</InfoValue>
        </InfoRow>
        
        <InfoRow>
          <span style={{fontSize: '20px', color: '#2E7D32'}}>✓</span>
          <InfoLabel>완료 시간:</InfoLabel>
          <InfoValue>{new Date().toLocaleString()}</InfoValue>
        </InfoRow>
        
        <InfoRow>
          <span style={{fontSize: '20px', color: '#2E7D32'}}>✓</span>
          <InfoLabel>골프공 감지:</InfoLabel>
          <InfoValue>성공</InfoValue>
        </InfoRow>
        
        <InfoRow>
          <span style={{fontSize: '20px', color: '#2E7D32'}}>✓</span>
          <InfoLabel>궤적 포인트:</InfoLabel>
          <InfoValue>42개 지점</InfoValue>
        </InfoRow>
      </InfoContainer>

      {/* Action Buttons */}
      <ActionContainer>
        <SaveButton onClick={handleSaveToGallery}>
          <span style={{fontSize: '24px'}}>💾</span>
          갤러리에 저장
        </SaveButton>

        <ShareButton onClick={handleShare}>
          <span style={{fontSize: '24px'}}>📤</span>
          공유하기
        </ShareButton>
      </ActionContainer>

      {/* Navigation to Gallery */}
      <GalleryButton onClick={handleGoToGallery}>
        <GalleryButtonLeft>
          <span style={{fontSize: '24px', color: '#2E7D32'}}>📁</span>
          <GalleryButtonText>
            내 스윙영상 보러가기
          </GalleryButtonText>
        </GalleryButtonLeft>
        <span style={{fontSize: '20px', color: '#2E7D32'}}>→</span>
      </GalleryButton>

      {/* Tips */}
      <TipsContainer>
        <TipsTitle>분석 결과 활용 팁</TipsTitle>
        
        <TipItem>
          <span style={{color: '#2E7D32'}}>•</span>
          <TipText>
            궤적을 통해 스윙의 일관성을 확인할 수 있습니다.
          </TipText>
        </TipItem>
        
        <TipItem>
          <span style={{color: '#2E7D32'}}>•</span>
          <TipText>
            영상을 반복 재생하며 개선점을 찾아보세요.
          </TipText>
        </TipItem>
        
        <TipItem>
          <span style={{color: '#2E7D32'}}>•</span>
          <TipText>
            친구들과 공유하여 피드백을 받아보세요.
          </TipText>
        </TipItem>
      </TipsContainer>
    </Container>
  );
};

export default ResultScreen;