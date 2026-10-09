import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useTranslation } from 'react-i18next';

type MainScreenNavigationProp = StackNavigationProp<RootStackParamList>;

const { width } = Dimensions.get('window');

const MainScreen: React.FC = () => {
  const navigation = useNavigation<MainScreenNavigationProp>();
  const { t } = useTranslation();

  const handleBallTracking = () => {
    // CLAUDE.md Step 5: "Ball Tracking" 선택 시, 사용자는 본인의 골프 영상을 업로드 함
    console.log('Step 4: 메인 화면에서 Ball Tracking 선택');
    navigation.navigate('BallTracking');
  };

  const handleSwingRecording = () => {
    // CLAUDE.md Step 2: 향후 구현할 기능 (본 앱의 영상촬영을 통해 확보된 영상에 골프공 궤적을 추가)
    console.log('Step 4: 메인 화면에서 Swing Recording 선택 (향후 구현)');
    navigation.navigate('SwingRecording');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header - CLAUDE.md Step 4: 유저정보 등도 우측 상단에 나오는 구조 */}
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <Text style={styles.greeting}>{t('main.greeting')}</Text>
            <Text style={styles.username}>Test User</Text>
            <Text style={styles.userStatus}>자동 로그인됨</Text>
          </View>
          <View style={styles.headerRight}>
            <View style={styles.userInfo}>
              <Text style={styles.userLabel}>Test User</Text>
              <Text style={styles.userSubtext}>임시 사용자</Text>
            </View>
            <TouchableOpacity style={styles.profileButton}>
              <Icon name="person" size={32} color="#2E7D32" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Main Content */}
        <View style={styles.content}>
          <Text style={styles.sectionTitle}>{t('main.features')}</Text>
          
          {/* Main Feature Buttons */}
          {/* CLAUDE.md Step 4: "Ball Tracking" 과 "Swing Recording" 두 개 큰 아이콘 */}
          <View style={styles.featureContainer}>
            <TouchableOpacity 
              style={styles.featureButton}
              onPress={handleBallTracking}
              activeOpacity={0.8}
            >
              <View style={styles.featureIconContainer}>
                <Icon name="track-changes" size={48} color="#FFFFFF" />
              </View>
              <Text style={styles.featureTitle}>{t('main.ballTracking')}</Text>
              <Text style={styles.featureDescription}>
                {t('main.ballTrackingDesc')}
              </Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={styles.featureButton}
              onPress={handleSwingRecording}
              activeOpacity={0.8}
            >
              <View style={styles.featureIconContainer}>
                <Icon name="videocam" size={48} color="#FFFFFF" />
              </View>
              <Text style={styles.featureTitle}>{t('main.swingRecording')}</Text>
              <Text style={styles.featureDescription}>
                {t('main.swingRecordingDesc')}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Quick Access Section */}
          <View style={styles.quickAccessContainer}>
            <Text style={styles.sectionTitle}>{t('main.quickAccess')}</Text>
            
            <View style={styles.quickAccessRow}>
              <TouchableOpacity style={styles.quickAccessButton}>
                <Icon name="video-library" size={24} color="#2E7D32" />
                <Text style={styles.quickAccessText}>{t('main.mySwings')}</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.quickAccessButton}>
                <Icon name="settings" size={24} color="#2E7D32" />
                <Text style={styles.quickAccessText}>{t('main.settings')}</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.quickAccessButton}>
                <Icon name="help" size={24} color="#2E7D32" />
                <Text style={styles.quickAccessText}>{t('main.help')}</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  scrollContent: {
    flexGrow: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 20,
    backgroundColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  headerLeft: {
    flex: 1,
  },
  greeting: {
    fontSize: 16,
    color: '#666666',
    marginBottom: 4,
  },
  username: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  userInfo: {
    alignItems: 'flex-end',
    marginRight: 12,
  },
  userLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2E7D32',
  },
  userSubtext: {
    fontSize: 12,
    color: '#666666',
    marginTop: 2,
  },
  userStatus: {
    fontSize: 12,
    color: '#4CAF50',
    marginTop: 2,
  },
  profileButton: {
    padding: 8,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 30,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333333',
    marginBottom: 20,
  },
  featureContainer: {
    marginBottom: 30,
  },
  featureButton: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 24,
    marginBottom: 16,
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
  featureIconContainer: {
    backgroundColor: '#2E7D32',
    borderRadius: 32,
    padding: 20,
    marginBottom: 16,
  },
  featureTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 8,
    textAlign: 'center',
  },
  featureDescription: {
    fontSize: 14,
    color: '#666666',
    textAlign: 'center',
    lineHeight: 20,
  },
  quickAccessContainer: {
    marginTop: 20,
  },
  quickAccessRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  quickAccessButton: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    flex: 1,
    marginHorizontal: 4,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  quickAccessText: {
    fontSize: 12,
    color: '#2E7D32',
    marginTop: 8,
    textAlign: 'center',
    fontWeight: '600',
  },
});

export default MainScreen;