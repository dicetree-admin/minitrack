import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Image,
  Dimensions,
  RefreshControl,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useTranslation } from 'react-i18next';

const { width } = Dimensions.get('window');
const ITEM_WIDTH = (width - 60) / 2;

interface VideoItem {
  id: string;
  title: string;
  thumbnail: string;
  duration: string;
  processedAt: string;
  processingId: string;
}

const VideoGalleryScreen: React.FC = () => {
  const { t } = useTranslation();
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  const mockVideos: VideoItem[] = [
    {
      id: '1',
      title: 'Golf Swing 2024-01-15',
      thumbnail: 'https://images.unsplash.com/photo-1530549387789-4c1017266635?w=300&h=200&fit=crop',
      duration: '00:08',
      processedAt: '2024-01-15 14:30',
      processingId: 'track_20240115_143000',
    },
    {
      id: '2',
      title: 'Practice Session',
      thumbnail: 'https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=300&h=200&fit=crop',
      duration: '00:12',
      processedAt: '2024-01-14 10:15',
      processingId: 'track_20240114_101500',
    },
  ];

  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    // CLAUDE.md 공통1: 본인이 업로드 한 영상의 작업물을 볼 수 있는 "내 스윙영상" 갤러리
    try {
      // In a real app, this would fetch from backend
      setVideos(mockVideos);
    } catch (error) {
      console.error('Failed to load videos:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadVideos();
    setRefreshing(false);
  };

  const renderVideoItem = ({ item }: { item: VideoItem }) => (
    <TouchableOpacity
      style={styles.videoItem}
      activeOpacity={0.8}
      onPress={() => {
        // Navigate to video player or result screen
        console.log('Playing video:', item.id);
      }}
    >
      <Image source={{ uri: item.thumbnail }} style={styles.thumbnail} />
      
      <View style={styles.playOverlay}>
        <Icon name="play-circle-fill" size={32} color="rgba(255, 255, 255, 0.9)" />
      </View>
      
      <View style={styles.durationBadge}>
        <Text style={styles.durationText}>{item.duration}</Text>
      </View>
      
      <View style={styles.videoInfo}>
        <Text style={styles.videoTitle} numberOfLines={2}>
          {item.title}
        </Text>
        <Text style={styles.videoDate}>
          {item.processedAt}
        </Text>
      </View>
      
      <TouchableOpacity
        style={styles.shareButton}
        onPress={(e) => {
          e.stopPropagation();
          // CLAUDE.md 공통2: 카카오톡을 통해 다른 사용자에게 공유 가능
          handleShare(item);
        }}
      >
        <Icon name="share" size={20} color="#2E7D32" />
      </TouchableOpacity>
    </TouchableOpacity>
  );

  const handleShare = (video: VideoItem) => {
    // Implement sharing functionality
    console.log('Sharing video:', video.id);
  };

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Icon name="video-library" size={64} color="#CCCCCC" />
      <Text style={styles.emptyTitle}>No Videos Yet</Text>
      <Text style={styles.emptyDescription}>
        Start tracking your golf swings to see them here
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>My Swing Videos</Text>
        <Text style={styles.subtitle}>
          {videos.length} video{videos.length !== 1 ? 's' : ''}
        </Text>
      </View>
      
      {videos.length > 0 ? (
        <FlatList
          data={videos}
          renderItem={renderVideoItem}
          keyExtractor={(item) => item.id}
          numColumns={2}
          columnWrapperStyle={styles.row}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor="#2E7D32"
              colors={['#2E7D32']}
            />
          }
        />
      ) : (
        renderEmptyState()
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: '#666666',
  },
  listContent: {
    padding: 20,
  },
  row: {
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  videoItem: {
    width: ITEM_WIDTH,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  thumbnail: {
    width: '100%',
    height: 120,
    backgroundColor: '#E0E0E0',
  },
  playOverlay: {
    position: 'absolute',
    top: 50,
    left: ITEM_WIDTH / 2 - 16,
    width: 32,
    height: 32,
    alignItems: 'center',
    justifyContent: 'center',
  },
  durationBadge: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  durationText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  videoInfo: {
    padding: 12,
    paddingBottom: 8,
  },
  videoTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333333',
    marginBottom: 4,
    lineHeight: 18,
  },
  videoDate: {
    fontSize: 12,
    color: '#666666',
  },
  shareButton: {
    position: 'absolute',
    bottom: 8,
    right: 8,
    padding: 4,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 40,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#666666',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyDescription: {
    fontSize: 16,
    color: '#999999',
    textAlign: 'center',
    lineHeight: 24,
  },
});

export default VideoGalleryScreen;