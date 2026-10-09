import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ScrollView,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { launchImageLibrary, MediaType, ImagePickerResponse } from 'react-native-image-picker';
import * as Progress from 'react-native-progress';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useTranslation } from 'react-i18next';

type BallTrackingScreenNavigationProp = StackNavigationProp<RootStackParamList, 'BallTracking'>;

const { width } = Dimensions.get('window');

interface ProcessingStatus {
  stage: string;
  progress: number;
  message: string;
}

const BallTrackingScreen: React.FC = () => {
  const navigation = useNavigation<BallTrackingScreenNavigationProp>();
  const { t } = useTranslation();
  
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatus>({
    stage: '',
    progress: 0,
    message: '',
  });

  const selectVideo = useCallback(() => {
    // CLAUDE.md Step 5: "Ball Tracking" 선택 시, 사용자는 본인의 골프 영상을 업로드 함
    console.log('Step 5: Ball Tracking 화면에서 영상 선택 시작');
    
    const options = {
      mediaType: 'video' as MediaType,
      quality: 0.8,
      videoQuality: 'high',
    };

    launchImageLibrary(options, (response: ImagePickerResponse) => {
      if (response.didCancel || response.errorMessage) {
        console.log('영상 선택 취소 또는 오류:', response.errorMessage);
        return;
      }

      if (response.assets && response.assets[0]) {
        const asset = response.assets[0];
        console.log('Step 5: 골프 영상 선택 완료:', asset.fileName);
        console.log('영상 크기:', asset.fileSize, 'bytes');
        console.log('영상 길이:', asset.duration, 'seconds');
        setSelectedVideo(asset.uri || null);
      }
    });
  }, []);

  const processVideo = useCallback(async () => {
    if (!selectedVideo) {
      Alert.alert(t('error.title'), t('ballTracking.selectVideoError'));
      return;
    }

    setIsProcessing(true);
    
    try {
      // CLAUDE.md Step 6: 영상이 서버로 업로드 되면 골프공 궤적 분석 백엔드 기능을 수행함
      
      // Step 1: Upload video
      setProcessingStatus({
        stage: 'upload',
        progress: 10,
        message: t('ballTracking.uploading'),
      });

      const formData = new FormData();
      formData.append('file', {
        uri: selectedVideo,
        type: 'video/mp4',
        name: 'golf_swing.mp4',
      } as any);

      const response = await fetch('http://localhost:8000/upload-video', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();

      // Simulate processing stages with progress updates
      const stages = [
        { stage: 'extracting', progress: 25, message: t('ballTracking.extractingFrames') },
        { stage: 'stabilizing', progress: 50, message: t('ballTracking.stabilizing') },
        { stage: 'detecting', progress: 75, message: t('ballTracking.detectingBall') },
        { stage: 'tracking', progress: 90, message: t('ballTracking.trackingTrajectory') },
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
      navigation.navigate('Result', {
        processingId: result.processing_id,
        videoUrl: result.result_video_url,
      });

    } catch (error) {
      console.error('Video processing error:', error);
      Alert.alert(
        t('error.title'),
        t('ballTracking.processingError')
      );
    } finally {
      setIsProcessing(false);
      setProcessingStatus({
        stage: '',
        progress: 0,
        message: '',
      });
    }
  }, [selectedVideo, navigation, t]);

  const renderUploadSection = () => (
    <View style={styles.uploadSection}>
      <Icon name="cloud-upload" size={64} color="#2E7D32" />
      <Text style={styles.uploadTitle}>{t('ballTracking.uploadTitle')}</Text>
      <Text style={styles.uploadDescription}>
        {t('ballTracking.uploadDescription')}
      </Text>
      
      <TouchableOpacity
        style={styles.selectButton}
        onPress={selectVideo}
        activeOpacity={0.8}
      >
        <Icon name="video-library" size={24} color="#FFFFFF" />
        <Text style={styles.selectButtonText}>
          {t('ballTracking.selectVideo')}
        </Text>
      </TouchableOpacity>

      {selectedVideo && (
        <View style={styles.selectedVideoContainer}>
          <Icon name="check-circle" size={24} color="#4CAF50" />
          <Text style={styles.selectedVideoText}>
            {t('ballTracking.videoSelected')}
          </Text>
        </View>
      )}
    </View>
  );

  const renderProcessingSection = () => (
    <View style={styles.processingSection}>
      <ActivityIndicator size="large" color="#2E7D32" />
      <Text style={styles.processingTitle}>
        {t('ballTracking.processing')}
      </Text>
      
      <View style={styles.progressContainer}>
        <Progress.Bar
          progress={processingStatus.progress / 100}
          width={width - 80}
          height={8}
          color="#2E7D32"
          unfilledColor="#E0E0E0"
          borderWidth={0}
          borderRadius={4}
        />
        <Text style={styles.progressText}>
          {Math.round(processingStatus.progress)}%
        </Text>
      </View>
      
      <Text style={styles.processingMessage}>
        {processingStatus.message}
      </Text>

      {/* Processing Steps Information */}
      <View style={styles.stepsContainer}>
        <Text style={styles.stepsTitle}>{t('ballTracking.processingSteps')}</Text>
        
        <View style={styles.stepItem}>
          <Icon name="movie" size={20} color="#666" />
          <Text style={styles.stepText}>{t('ballTracking.step1')}</Text>
        </View>
        
        <View style={styles.stepItem}>
          <Icon name="tune" size={20} color="#666" />
          <Text style={styles.stepText}>{t('ballTracking.step2')}</Text>
        </View>
        
        <View style={styles.stepItem}>
          <Icon name="search" size={20} color="#666" />
          <Text style={styles.stepText}>{t('ballTracking.step3')}</Text>
        </View>
        
        <View style={styles.stepItem}>
          <Icon name="timeline" size={20} color="#666" />
          <Text style={styles.stepText}>{t('ballTracking.step4')}</Text>
        </View>
      </View>
    </View>
  );

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      {!isProcessing ? (
        <>
          {renderUploadSection()}
          
          {selectedVideo && (
            <TouchableOpacity
              style={styles.processButton}
              onPress={processVideo}
              activeOpacity={0.8}
            >
              <Icon name="play-arrow" size={24} color="#FFFFFF" />
              <Text style={styles.processButtonText}>
                {t('ballTracking.startProcessing')}
              </Text>
            </TouchableOpacity>
          )}
          
          {/* Instructions */}
          <View style={styles.instructionsContainer}>
            <Text style={styles.instructionsTitle}>
              {t('ballTracking.instructions')}
            </Text>
            
            <View style={styles.instructionItem}>
              <Icon name="fiber-manual-record" size={8} color="#2E7D32" />
              <Text style={styles.instructionText}>
                {t('ballTracking.instruction1')}
              </Text>
            </View>
            
            <View style={styles.instructionItem}>
              <Icon name="fiber-manual-record" size={8} color="#2E7D32" />
              <Text style={styles.instructionText}>
                {t('ballTracking.instruction2')}
              </Text>
            </View>
            
            <View style={styles.instructionItem}>
              <Icon name="fiber-manual-record" size={8} color="#2E7D32" />
              <Text style={styles.instructionText}>
                {t('ballTracking.instruction3')}
              </Text>
            </View>
          </View>
        </>
      ) : (
        renderProcessingSection()
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  scrollContent: {
    flexGrow: 1,
    padding: 20,
  },
  uploadSection: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 32,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 8,
  },
  uploadTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginTop: 16,
    marginBottom: 8,
    textAlign: 'center',
  },
  uploadDescription: {
    fontSize: 16,
    color: '#666666',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 24,
  },
  selectButton: {
    backgroundColor: '#2E7D32',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    flexDirection: 'row',
    alignItems: 'center',
  },
  selectButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  selectedVideoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
    padding: 12,
    backgroundColor: '#E8F5E8',
    borderRadius: 8,
  },
  selectedVideoText: {
    color: '#2E7D32',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  processButton: {
    backgroundColor: '#4CAF50',
    borderRadius: 12,
    paddingVertical: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  processButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  processingSection: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 32,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 8,
  },
  processingTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginTop: 16,
    marginBottom: 24,
  },
  progressContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  progressText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginTop: 8,
  },
  processingMessage: {
    fontSize: 16,
    color: '#666666',
    textAlign: 'center',
    marginBottom: 32,
  },
  stepsContainer: {
    alignSelf: 'stretch',
  },
  stepsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333333',
    marginBottom: 16,
  },
  stepItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  stepText: {
    fontSize: 14,
    color: '#666666',
    marginLeft: 12,
    flex: 1,
  },
  instructionsContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  instructionsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333333',
    marginBottom: 16,
  },
  instructionItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  instructionText: {
    fontSize: 14,
    color: '#666666',
    marginLeft: 12,
    flex: 1,
    lineHeight: 20,
  },
});

export default BallTrackingScreen;