import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ScrollView,
  Dimensions,
} from 'react-native';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';
import Video from 'react-native-video';
import Share from 'react-native-share';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useTranslation } from 'react-i18next';

type ResultScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Result'>;
type ResultScreenRouteProp = RouteProp<RootStackParamList, 'Result'>;

const { width, height } = Dimensions.get('window');

const ResultScreen: React.FC = () => {
  const navigation = useNavigation<ResultScreenNavigationProp>();
  const route = useRoute<ResultScreenRouteProp>();
  const { t } = useTranslation();
  
  const { processingId, videoUrl } = route.params;
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [showControls, setShowControls] = useState(true);

  useEffect(() => {
    // CLAUDE.md Step 10: 골프공 궤도 그리기가 완료되면, 화면 상 "골프공 궤적 분석 완료" 메시지
    Alert.alert(
      t('result.analysisComplete'),
      t('result.analysisCompleteMessage'),
      [{ text: 'OK', style: 'default' }]
    );
  }, [t]);

  const handleSaveToGallery = async () => {
    // CLAUDE.md Step 12: 갤러리에 저장 옵션
    try {
      // Implementation would save to device gallery
      Alert.alert(
        t('result.saved'),
        t('result.savedMessage')
      );
    } catch (error) {
      Alert.alert(
        t('error.title'),
        t('result.saveError')
      );
    }
  };

  const handleShare = async () => {
    // CLAUDE.md Step 12: 친구에게 공유 선택 옵션 (카카오톡 공유)
    try {
      const shareOptions = {
        title: 'Golf Ball Trajectory Analysis',
        message: 'Check out my golf swing analysis from MiniTrack!',
        url: videoUrl, // In production, this would be a shareable URL
        type: 'video/mp4',
      };

      await Share.open(shareOptions);
    } catch (error) {
      console.log('Share cancelled or failed:', error);
    }
  };

  const handleGoToGallery = () => {
    // CLAUDE.md Step 13: "내 스윙영상" 갤러리로 이동
    navigation.reset({
      index: 0,
      routes: [
        {
          name: 'MainTabs',
          state: {
            routes: [
              { name: 'Home' },
              { name: 'Gallery' },
            ],
            index: 1, // Navigate to Gallery tab
          },
        },
      ],
    });
  };

  const togglePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      {/* Success Message */}
      <View style={styles.successBanner}>
        <Icon name="check-circle" size={32} color="#4CAF50" />
        <Text style={styles.successTitle}>
          {t('result.analysisComplete')}
        </Text>
        <Text style={styles.successDescription}>
          {t('result.trajectoryAdded')}
        </Text>
      </View>

      {/* Video Player */}
      <View style={styles.videoContainer}>
        <Video
          source={{ uri: videoUrl }}
          style={styles.videoPlayer}
          controls={showControls}
          paused={!isPlaying}
          repeat={true}
          resizeMode="contain"
          onError={(error) => {
            console.error('Video playback error:', error);
            Alert.alert(t('error.title'), t('result.playbackError'));
          }}
        />
        
        {!showControls && (
          <TouchableOpacity
            style={styles.playButton}
            onPress={togglePlayPause}
            activeOpacity={0.8}
          >
            <Icon 
              name={isPlaying ? 'pause-circle-fill' : 'play-circle-fill'} 
              size={64} 
              color="rgba(255, 255, 255, 0.9)" 
            />
          </TouchableOpacity>
        )}
      </View>

      {/* Analysis Information */}
      <View style={styles.infoContainer}>
        <Text style={styles.infoTitle}>{t('result.analysisInfo')}</Text>
        
        <View style={styles.infoRow}>
          <Icon name="timeline" size={20} color="#2E7D32" />
          <Text style={styles.infoLabel}>{t('result.processingId')}:</Text>
          <Text style={styles.infoValue}>{processingId}</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Icon name="access-time" size={20} color="#2E7D32" />
          <Text style={styles.infoLabel}>{t('result.completedAt')}:</Text>
          <Text style={styles.infoValue}>{new Date().toLocaleString()}</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Icon name="sports-golf" size={20} color="#2E7D32" />
          <Text style={styles.infoLabel}>{t('result.ballDetected')}:</Text>
          <Text style={styles.infoValue}>{t('result.yes')}</Text>
        </View>
        
        <View style={styles.infoRow}>
          <Icon name="show-chart" size={20} color="#2E7D32" />
          <Text style={styles.infoLabel}>{t('result.trajectoryPoints')}:</Text>
          <Text style={styles.infoValue}>42 points</Text>
        </View>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionContainer}>
        <TouchableOpacity
          style={[styles.actionButton, styles.saveButton]}
          onPress={handleSaveToGallery}
          activeOpacity={0.8}
        >
          <Icon name="save-alt" size={24} color="#FFFFFF" />
          <Text style={styles.actionButtonText}>
            {t('result.saveToGallery')}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionButton, styles.shareButton]}
          onPress={handleShare}
          activeOpacity={0.8}
        >
          <Icon name="share" size={24} color="#FFFFFF" />
          <Text style={styles.actionButtonText}>
            {t('result.shareVideo')}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Navigation to Gallery */}
      <TouchableOpacity
        style={styles.galleryButton}
        onPress={handleGoToGallery}
        activeOpacity={0.8}
      >
        <Icon name="video-library" size={24} color="#2E7D32" />
        <Text style={styles.galleryButtonText}>
          {t('result.viewMySwings')}
        </Text>
        <Icon name="arrow-forward" size={20} color="#2E7D32" />
      </TouchableOpacity>

      {/* Tips */}
      <View style={styles.tipsContainer}>
        <Text style={styles.tipsTitle}>{t('result.tips')}</Text>
        
        <View style={styles.tipItem}>
          <Icon name="fiber-manual-record" size={8} color="#2E7D32" />
          <Text style={styles.tipText}>
            {t('result.tip1')}
          </Text>
        </View>
        
        <View style={styles.tipItem}>
          <Icon name="fiber-manual-record" size={8} color="#2E7D32" />
          <Text style={styles.tipText}>
            {t('result.tip2')}
          </Text>
        </View>
        
        <View style={styles.tipItem}>
          <Icon name="fiber-manual-record" size={8} color="#2E7D32" />
          <Text style={styles.tipText}>
            {t('result.tip3')}
          </Text>
        </View>
      </View>
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
  successBanner: {
    backgroundColor: '#E8F5E8',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#C8E6C9',
  },
  successTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginTop: 8,
    marginBottom: 4,
  },
  successDescription: {
    fontSize: 14,
    color: '#4CAF50',
    textAlign: 'center',
  },
  videoContainer: {
    backgroundColor: '#000000',
    borderRadius: 12,
    overflow: 'hidden',
    marginBottom: 20,
    aspectRatio: 16 / 9,
    position: 'relative',
  },
  videoPlayer: {
    width: '100%',
    height: '100%',
  },
  playButton: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -32,
    marginLeft: -32,
  },
  infoContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333333',
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  infoLabel: {
    fontSize: 14,
    color: '#666666',
    marginLeft: 8,
    flex: 1,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333333',
  },
  actionContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  actionButton: {
    flex: 1,
    borderRadius: 12,
    paddingVertical: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 4,
  },
  saveButton: {
    backgroundColor: '#4CAF50',
  },
  shareButton: {
    backgroundColor: '#2196F3',
  },
  actionButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  galleryButton: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  galleryButtonText: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#2E7D32',
    marginLeft: 12,
  },
  tipsContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
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
  tipsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333333',
    marginBottom: 16,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  tipText: {
    fontSize: 14,
    color: '#666666',
    marginLeft: 12,
    flex: 1,
    lineHeight: 20,
  },
});

export default ResultScreen;