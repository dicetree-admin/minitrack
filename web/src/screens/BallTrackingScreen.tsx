import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
// Using emoji icons for simplicity

const Container = styled.div`
  min-height: 100vh;
  background: #F5F5F5;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
`;

const UploadSection = styled.div`
  background: white;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
`;

const UploadIcon = styled.div`
  margin-bottom: 16px;
`;

const UploadTitle = styled.h2`
  font-size: 24px;
  font-weight: bold;
  color: #2E7D32;
  margin-bottom: 8px;
`;

const UploadDescription = styled.p`
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
  line-height: 1.5;
`;

const SelectButton = styled.button`
  background: #2E7D32;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  margin: 0 auto;
  transition: background 0.2s ease;

  &:hover {
    background: #1B5E20;
  }
`;

const SelectedVideoContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px;
  background: #E8F5E8;
  border-radius: 8px;
`;

const SelectedVideoText = styled.span`
  color: #2E7D32;
  font-size: 14px;
  font-weight: 600;
`;

const ProcessButton = styled.button`
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  width: 100%;
  margin-bottom: 20px;
  transition: background 0.2s ease;

  &:hover {
    background: #388E3C;
  }
`;

const ProcessingSection = styled.div`
  background: white;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
`;

const ProcessingTitle = styled.h2`
  font-size: 24px;
  font-weight: bold;
  color: #2E7D32;
  margin: 16px 0 24px 0;
`;

const ProgressContainer = styled.div`
  margin-bottom: 20px;
`;

const ProgressBar = styled.div<{ progress: number }>`
  width: 100%;
  height: 8px;
  background: #E0E0E0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
  
  &::after {
    content: '';
    display: block;
    width: ${props => props.progress}%;
    height: 100%;
    background: #2E7D32;
    transition: width 0.3s ease;
  }
`;

const ProgressText = styled.p`
  font-size: 16px;
  font-weight: bold;
  color: #2E7D32;
  margin: 0;
`;

const ProcessingMessage = styled.p`
  font-size: 16px;
  color: #666;
  margin-bottom: 32px;
`;

const StepsContainer = styled.div`
  text-align: left;
`;

const StepsTitle = styled.h3`
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
`;

const StepItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
`;

const StepText = styled.span`
  font-size: 14px;
  color: #666;
  flex: 1;
`;

const InstructionsContainer = styled.div`
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const InstructionsTitle = styled.h3`
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
`;

const InstructionItem = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
`;

const InstructionText = styled.span`
  font-size: 14px;
  color: #666;
  flex: 1;
  line-height: 1.4;
`;

const HiddenInput = styled.input`
  display: none;
`;

interface ProcessingStatus {
  stage: string;
  progress: number;
  message: string;
}

const BallTrackingScreen: React.FC = () => {
  const navigate = useNavigate();
  
  const [selectedVideo, setSelectedVideo] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatus>({
    stage: '',
    progress: 0,
    message: '',
  });

  const selectVideo = useCallback(() => {
    // CLAUDE.md Step 5: "Ball Tracking" 선택 시, 사용자는 본인의 골프 영상을 업로드 함
    console.log('Step 5: Ball Tracking 화면에서 영상 선택 시작');
    
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'video/*';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        console.log('Step 5: 골프 영상 선택 완료:', file.name);
        console.log('영상 크기:', file.size, 'bytes');
        setSelectedVideo(file);
      }
    };
    input.click();
  }, []);

  const processVideo = useCallback(async () => {
    if (!selectedVideo) {
      alert('영상을 먼저 선택해주세요.');
      return;
    }

    setIsProcessing(true);
    
    try {
      // CLAUDE.md Step 6: 영상이 서버로 업로드 되면 골프공 궤적 분석 백엔드 기능을 수행함
      
      // Step 1: Upload video
      setProcessingStatus({
        stage: 'upload',
        progress: 10,
        message: '영상 업로드 중...',
      });

      const formData = new FormData();
      formData.append('file', selectedVideo);

      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();

      // Simulate processing stages with progress updates
      const stages = [
        { stage: 'extracting', progress: 25, message: '프레임 추출 중...' },
        { stage: 'stabilizing', progress: 50, message: '이미지 안정화 적용 중...' },
        { stage: 'detecting', progress: 75, message: '골프공 감지 중...' },
        { stage: 'tracking', progress: 90, message: '궤적 추적 중...' },
      ];

      for (const stage of stages) {
        setProcessingStatus(stage);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      // CLAUDE.md Step 10: 골프공 궤도 그리기가 완료되면, 화면 상 "골프공 궤적 분석 완료" 메시지가 뜸
      setProcessingStatus({
        stage: 'complete',
        progress: 100,
        message: result.message || '골프공 궤적 분석 완료',
      });
      
      // Show completion message for 2 seconds before navigating
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Navigate to result screen
      navigate('/result', {
        state: {
          processingId: result.processing_id || 'demo-' + Date.now(),
          videoUrl: result.result_video_url || '/demo-result-video.mp4',
          originalVideo: selectedVideo,
        }
      });

    } catch (error) {
      console.error('Video processing error:', error);
      alert('영상 처리 중 오류가 발생했습니다. 백엔드 서버가 실행 중인지 확인해주세요.');
    } finally {
      setIsProcessing(false);
      setProcessingStatus({
        stage: '',
        progress: 0,
        message: '',
      });
    }
  }, [selectedVideo, navigate]);

  const renderUploadSection = () => (
    <UploadSection>
      <UploadIcon>
        <span style={{fontSize: '64px'}}>☁️</span>
      </UploadIcon>
      <UploadTitle>골프 영상 업로드</UploadTitle>
      <UploadDescription>
        골프 스윙 영상을 선택하면 공의 궤적을 자동으로 분석하여 시각화해드립니다.
      </UploadDescription>
      
      <SelectButton onClick={selectVideo}>
        <span style={{fontSize: '24px'}}>🎥</span>
        영상 선택하기
      </SelectButton>

      {selectedVideo && (
        <SelectedVideoContainer>
          <span style={{fontSize: '24px', color: '#4CAF50'}}>✓</span>
          <SelectedVideoText>
            선택된 영상: {selectedVideo.name}
          </SelectedVideoText>
        </SelectedVideoContainer>
      )}
    </UploadSection>
  );

  const renderProcessingSection = () => (
    <ProcessingSection>
      <span style={{fontSize: '32px', color: '#2E7D32'}} className="fa-spin">⭕</span>
      <ProcessingTitle>
        영상 분석 중...
      </ProcessingTitle>
      
      <ProgressContainer>
        <ProgressBar progress={processingStatus.progress} />
        <ProgressText>
          {Math.round(processingStatus.progress)}%
        </ProgressText>
      </ProgressContainer>
      
      <ProcessingMessage>
        {processingStatus.message}
      </ProcessingMessage>

      {/* Processing Steps Information */}
      <StepsContainer>
        <StepsTitle>처리 단계</StepsTitle>
        
        <StepItem>
          <span style={{fontSize: '20px', color: '#666'}}>🎥</span>
          <StepText>1. 영상을 프레임별로 분할</StepText>
        </StepItem>
        
        <StepItem>
          <span style={{fontSize: '20px', color: '#666'}}>⚙️</span>
          <StepText>2. 이미지 안정화 적용</StepText>
        </StepItem>
        
        <StepItem>
          <span style={{fontSize: '20px', color: '#666'}}>✓</span>
          <StepText>3. 골프공 감지 및 추적</StepText>
        </StepItem>
        
        <StepItem>
          <span style={{fontSize: '20px', color: '#666'}}>▶️</span>
          <StepText>4. 궤적 시각화 및 영상 생성</StepText>
        </StepItem>
      </StepsContainer>
    </ProcessingSection>
  );

  return (
    <Container>
      {!isProcessing ? (
        <>
          {renderUploadSection()}
          
          {selectedVideo && (
            <ProcessButton onClick={processVideo}>
              <span style={{fontSize: '24px'}}>▶️</span>
              분석 시작하기
            </ProcessButton>
          )}
          
          {/* Instructions */}
          <InstructionsContainer>
            <InstructionsTitle>
              사용 안내
            </InstructionsTitle>
            
            <InstructionItem>
              <span style={{color: '#2E7D32'}}>•</span>
              <InstructionText>
                골프공이 명확하게 보이는 영상을 업로드해주세요.
              </InstructionText>
            </InstructionItem>
            
            <InstructionItem>
              <span style={{color: '#2E7D32'}}>•</span>
              <InstructionText>
                스윙 전체 구간이 포함된 영상이 좋습니다.
              </InstructionText>
            </InstructionItem>
            
            <InstructionItem>
              <span style={{color: '#2E7D32'}}>•</span>
              <InstructionText>
                처리 시간은 영상 길이에 따라 1-5분 소요됩니다.
              </InstructionText>
            </InstructionItem>
          </InstructionsContainer>
        </>
      ) : (
        renderProcessingSection()
      )}
    </Container>
  );
};

export default BallTrackingScreen;