import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  Alert,
  Dimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/apiService';
import CameraFeed from '../components/CameraFeed';

const { width } = Dimensions.get('window');

const CameraScreen = () => {
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedCamera, setSelectedCamera] = useState(null);

  useEffect(() => {
    loadCameras();
  }, []);

  const loadCameras = async () => {
    try {
      setLoading(true);
      const response = await apiService.getCameras();
      setCameras(response.data);
    } catch (error) {
      console.error('Failed to load cameras:', error);
      Alert.alert('Error', 'Failed to load cameras. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadCameras();
    setRefreshing(false);
  };

  const handleCameraPress = (camera) => {
    setSelectedCamera(camera);
  };

  const handleCameraControl = async (cameraId, action) => {
    try {
      if (action === 'start') {
        await apiService.startCamera(cameraId);
      } else if (action === 'stop') {
        await apiService.stopCamera(cameraId);
      }
      
      // Refresh camera list to get updated status
      await loadCameras();
    } catch (error) {
      console.error(`Failed to ${action} camera:`, error);
      Alert.alert('Error', `Failed to ${action} camera. Please try again.`);
    }
  };

  const renderCameraItem = ({ item }) => (
    <View style={styles.cameraCard}>
      <View style={styles.cameraHeader}>
        <View style={styles.cameraInfo}>
          <Text style={styles.cameraName}>{item.name}</Text>
          <Text style={styles.cameraLocation}>{item.location}</Text>
        </View>
        <View style={styles.statusContainer}>
          <View style={[
            styles.statusIndicator,
            { backgroundColor: item.status === 'online' ? '#4CAF50' : '#F44336' }
          ]} />
          <Text style={[
            styles.statusText,
            { color: item.status === 'online' ? '#4CAF50' : '#F44336' }
          ]}>
            {item.status}
          </Text>
        </View>
      </View>

      <TouchableOpacity
        style={styles.cameraFeedContainer}
        onPress={() => handleCameraPress(item)}
        activeOpacity={0.8}
      >
        <CameraFeed camera={item} />
      </TouchableOpacity>

      <View style={styles.cameraControls}>
        <TouchableOpacity
          style={[
            styles.controlButton,
            item.is_active ? styles.stopButton : styles.startButton
          ]}
          onPress={() => handleCameraControl(
            item.id,
            item.is_active ? 'stop' : 'start'
          )}
        >
          <Icon
            name={item.is_active ? 'stop' : 'play_arrow'}
            size={20}
            color="#FFFFFF"
          />
          <Text style={styles.controlButtonText}>
            {item.is_active ? 'Stop' : 'Start'}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.controlButton}
          onPress={() => handleCameraPress(item)}
        >
          <Icon name="fullscreen" size={20} color="#2196F3" />
          <Text style={[styles.controlButtonText, { color: '#2196F3' }]}>
            Fullscreen
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  const renderEmptyState = () => (
    <View style={styles.emptyState}>
      <Icon name="videocam-off" size={80} color="#BDBDBD" />
      <Text style={styles.emptyStateTitle}>No Cameras Available</Text>
      <Text style={styles.emptyStateText}>
        Add cameras to your system to start monitoring
      </Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Icon name="refresh" size={40} color="#2196F3" />
        <Text style={styles.loadingText}>Loading cameras...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Camera Feeds</Text>
        <TouchableOpacity style={styles.refreshButton} onPress={onRefresh}>
          <Icon name="refresh" size={24} color="#2196F3" />
        </TouchableOpacity>
      </View>

      <FlatList
        data={cameras}
        renderItem={renderCameraItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.cameraList}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={renderEmptyState}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  refreshButton: {
    padding: 8,
  },
  cameraList: {
    padding: 15,
  },
  cameraCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cameraHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  cameraInfo: {
    flex: 1,
  },
  cameraName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  cameraLocation: {
    fontSize: 12,
    color: '#666',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '500',
  },
  cameraFeedContainer: {
    height: 200,
    backgroundColor: '#000',
    borderRadius: 8,
    margin: 15,
    overflow: 'hidden',
  },
  cameraControls: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 15,
    paddingBottom: 15,
  },
  controlButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    backgroundColor: '#2196F3',
  },
  startButton: {
    backgroundColor: '#4CAF50',
  },
  stopButton: {
    backgroundColor: '#F44336',
  },
  controlButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '500',
    marginLeft: 5,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyStateTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginTop: 15,
    marginBottom: 8,
  },
  emptyStateText: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    paddingHorizontal: 40,
  },
});

export default CameraScreen; 