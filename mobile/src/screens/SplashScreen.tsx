import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ImageBackground,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useTranslation } from 'react-i18next';

type SplashScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Splash'>;

const { width, height } = Dimensions.get('window');

const SplashScreen: React.FC = () => {
  const navigation = useNavigation<SplashScreenNavigationProp>();
  const { t } = useTranslation();

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
          { message: 'Loading YOLO models...', duration: 1200 },
          { message: 'Preparing vision engine...', duration: 1000 },
        ];
        
        for (const step of loadingSteps) {
          console.log(`Backend Loading: ${step.message}`);
          await new Promise(resolve => setTimeout(resolve, step.duration));
        }
        
        // Check backend connectivity
        console.log('Checking backend connectivity...');
        try {
          const response = await fetch('http://localhost:8000/', {
            timeout: 5000
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
        navigation.replace('MainTabs');
        
      } catch (error) {
        console.error('앱 초기화 실패:', error);
        // Continue to main screen even if initialization fails
        navigation.replace('MainTabs');
      }
    };

    initializeApp();
  }, [navigation]);

  return (
    <View style={styles.container}>
      <ImageBackground
        source={{ uri: 'https://images.unsplash.com/photo-1530549387789-4c1017266635?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80' }}
        style={styles.background}
        resizeMode="cover"
      >
        <View style={styles.overlay}>
          <View style={styles.content}>
            <Text style={styles.title}>MiniTrack</Text>
            <Text style={styles.subtitle}>{t('splash.subtitle')}</Text>
            <Text style={styles.description}>
              {t('splash.description')}
            </Text>
            
            <ActivityIndicator 
              size="large" 
              color="#4CAF50" 
              style={styles.loader}
            />
            
            <Text style={styles.loadingText}>
              {t('splash.loading')}
            </Text>
          </View>
        </View>
      </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  background: {
    flex: 1,
    width: width,
    height: height,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  title: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 10,
    textShadowColor: 'rgba(0, 0, 0, 0.5)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 4,
  },
  subtitle: {
    fontSize: 18,
    color: '#4CAF50',
    marginBottom: 20,
    fontWeight: '600',
  },
  description: {
    fontSize: 16,
    color: '#FFFFFF',
    textAlign: 'center',
    marginBottom: 40,
    lineHeight: 24,
  },
  loader: {
    marginBottom: 20,
  },
  loadingText: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '500',
  },
});

export default SplashScreen;