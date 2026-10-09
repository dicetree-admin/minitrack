import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useTranslation } from 'react-i18next';

const SwingRecordingScreen: React.FC = () => {
  const { t } = useTranslation();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Icon name="videocam-off" size={80} color="#CCCCCC" />
        
        <Text style={styles.title}>
          Swing Recording
        </Text>
        
        <Text style={styles.description}>
          Real-time golf swing recording and analysis feature is coming soon!
        </Text>
        
        <View style={styles.featuresContainer}>
          <View style={styles.featureItem}>
            <Icon name="camera-alt" size={24} color="#2E7D32" />
            <Text style={styles.featureText}>Real-time recording</Text>
          </View>
          
          <View style={styles.featureItem}>
            <Icon name="auto-awesome" size={24} color="#2E7D32" />
            <Text style={styles.featureText}>Live ball tracking</Text>
          </View>
          
          <View style={styles.featureItem}>
            <Icon name="speed" size={24} color="#2E7D32" />
            <Text style={styles.featureText}>Instant analysis</Text>
          </View>
        </View>
        
        <TouchableOpacity
          style={styles.notifyButton}
          activeOpacity={0.8}
        >
          <Icon name="notifications" size={20} color="#FFFFFF" />
          <Text style={styles.notifyButtonText}>
            Notify me when available
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333333',
    marginTop: 20,
    marginBottom: 16,
  },
  description: {
    fontSize: 16,
    color: '#666666',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 40,
  },
  featuresContainer: {
    alignSelf: 'stretch',
    marginBottom: 40,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  featureText: {
    fontSize: 16,
    color: '#333333',
    marginLeft: 16,
    fontWeight: '600',
  },
  notifyButton: {
    backgroundColor: '#2E7D32',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    flexDirection: 'row',
    alignItems: 'center',
  },
  notifyButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default SwingRecordingScreen;