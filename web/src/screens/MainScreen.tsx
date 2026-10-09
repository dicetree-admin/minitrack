import React from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
// Using emoji icons for simplicity

const Container = styled.div`
  min-height: 100vh;
  background: #F5F5F5;
  padding: 0;
`;

const Header = styled.div`
  background: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const HeaderLeft = styled.div`
  flex: 1;
`;

const Greeting = styled.p`
  color: #666;
  margin: 0 0 4px 0;
  font-size: 16px;
`;

const Username = styled.h2`
  color: #2E7D32;
  margin: 0;
  font-size: 24px;
  font-weight: bold;
`;

const UserStatus = styled.p`
  color: #4CAF50;
  margin: 2px 0 0 0;
  font-size: 12px;
`;

const HeaderRight = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

const UserInfo = styled.div`
  text-align: right;
`;

const UserLabel = styled.p`
  color: #2E7D32;
  margin: 0;
  font-size: 14px;
  font-weight: 600;
`;

const UserSubtext = styled.p`
  color: #666;
  margin: 2px 0 0 0;
  font-size: 12px;
`;

const ProfileButton = styled.button`
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 50%;
  
  &:hover {
    background: rgba(46, 125, 50, 0.1);
  }
`;

const Content = styled.div`
  padding: 30px 20px;
`;

const SectionTitle = styled.h3`
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
`;

const FeatureContainer = styled.div`
  margin-bottom: 30px;
`;

const FeatureButton = styled.button`
  width: 100%;
  background: white;
  border: none;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }
`;

const FeatureIconContainer = styled.div`
  background: #2E7D32;
  border-radius: 32px;
  padding: 20px;
  margin-bottom: 16px;
`;

const FeatureTitle = styled.h4`
  font-size: 20px;
  font-weight: bold;
  color: #2E7D32;
  margin: 0 0 8px 0;
  text-align: center;
`;

const FeatureDescription = styled.p`
  font-size: 14px;
  color: #666;
  text-align: center;
  line-height: 1.4;
  margin: 0;
`;

const QuickAccessContainer = styled.div`
  margin-top: 20px;
`;

const QuickAccessRow = styled.div`
  display: flex;
  gap: 8px;
`;

const QuickAccessButton = styled.button`
  flex: 1;
  background: white;
  border: none;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-1px);
  }
`;

const QuickAccessText = styled.p`
  font-size: 12px;
  color: #2E7D32;
  margin: 8px 0 0 0;
  text-align: center;
  font-weight: 600;
`;

const MainScreen: React.FC = () => {
  const navigate = useNavigate();

  const handleBallTracking = () => {
    // CLAUDE.md Step 5: "Ball Tracking" 선택 시, 사용자는 본인의 골프 영상을 업로드 함
    console.log('Step 4: 메인 화면에서 Ball Tracking 선택');
    navigate('/ball-tracking');
  };

  const handleSwingRecording = () => {
    // CLAUDE.md Step 2: 향후 구현할 기능 (본 앱의 영상촬영을 통해 확보된 영상에 골프공 궤적을 추가)
    console.log('Step 4: 메인 화면에서 Swing Recording 선택 (향후 구현)');
    alert('향후 구현 예정인 기능입니다.');
  };

  const handleMySwings = () => {
    navigate('/gallery');
  };

  return (
    <Container>
      {/* Header - CLAUDE.md Step 4: 유저정보 등도 우측 상단에 나오는 구조 */}
      <Header>
        <HeaderLeft>
          <Greeting>안녕하세요!</Greeting>
          <Username>Test User</Username>
          <UserStatus>자동 로그인됨</UserStatus>
        </HeaderLeft>
        <HeaderRight>
          <UserInfo>
            <UserLabel>Test User</UserLabel>
            <UserSubtext>임시 사용자</UserSubtext>
          </UserInfo>
          <ProfileButton>
            <span style={{fontSize: '32px'}}>👤</span>
          </ProfileButton>
        </HeaderRight>
      </Header>

      {/* Main Content */}
      <Content>
        <SectionTitle>주요 기능</SectionTitle>
        
        {/* Main Feature Buttons */}
        {/* CLAUDE.md Step 4: "Ball Tracking" 과 "Swing Recording" 두 개 큰 아이콘 */}
        <FeatureContainer>
          <FeatureButton onClick={handleBallTracking}>
            <FeatureIconContainer>
              <span style={{fontSize: '48px'}}>⚪</span>
            </FeatureIconContainer>
            <FeatureTitle>Ball Tracking</FeatureTitle>
            <FeatureDescription>
              골프 영상을 업로드하여 공의 궤적을 분석하고 시각화합니다.
            </FeatureDescription>
          </FeatureButton>

          <FeatureButton onClick={handleSwingRecording}>
            <FeatureIconContainer>
              <span style={{fontSize: '48px'}}>🎥</span>
            </FeatureIconContainer>
            <FeatureTitle>Swing Recording</FeatureTitle>
            <FeatureDescription>
              앱에서 직접 골프 스윙을 촬영하고 궤적을 분석합니다. (향후 구현)
            </FeatureDescription>
          </FeatureButton>
        </FeatureContainer>

        {/* Quick Access Section */}
        <SectionTitle>빠른 액세스</SectionTitle>
        <QuickAccessContainer>
          <QuickAccessRow>
            <QuickAccessButton onClick={handleMySwings}>
              <span style={{fontSize: '24px'}}>📁</span>
              <QuickAccessText>내 스윙영상</QuickAccessText>
            </QuickAccessButton>
            
            <QuickAccessButton>
              <span style={{fontSize: '24px'}}>⚙️</span>
              <QuickAccessText>설정</QuickAccessText>
            </QuickAccessButton>
            
            <QuickAccessButton>
              <span style={{fontSize: '24px'}}>❓</span>
              <QuickAccessText>도움말</QuickAccessText>
            </QuickAccessButton>
          </QuickAccessRow>
        </QuickAccessContainer>
      </Content>
    </Container>
  );
};

export default MainScreen;