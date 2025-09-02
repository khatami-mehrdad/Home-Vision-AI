import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  ActivityIndicator,
  TouchableOpacity,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/apiService';

const CameraFeed = ({ camera }) => {
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    if (camera && camera.is_active) {
      loadCameraFrame();
      // Set up periodic refresh every 5 seconds
      const interval = setInterval(loadCameraFrame, 5000);
      return () => clearInterval(interval);
    }
  }, [camera]);

  const loadCameraFrame = async () => {
    if (!camera || !camera.is_active) {
      setLoading(false);
      setError(true);
      return;
    }

    try {
      setLoading(true);
      setError(false);
      
      const response = await apiService.getCameraFrame(camera.id);
      
      if (response.status === 200) {
        // Create blob URL for the image
        const blob = new Blob([response.data], { type: 'image/jpeg' });
        const url = URL.createObjectURL(blob);
        setImageUrl(url);
        setLastUpdated(new Date());
      } else {
        setError(true);
      }
    } catch (error) {
      console.error('Failed to load camera frame:', error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  const renderPlaceholder = () => (
    <View style={styles.placeholder}>
      <Icon name="videocam-off" size={40} color="#BDBDBD" />
      <Text style={styles.placeholderText}>
        {camera?.is_active ? 'Camera Offline' : 'Camera Inactive'}
      </Text>
      {camera?.is_active && (
        <TouchableOpacity style={styles.retryButton} onPress={loadCameraFrame}>
          <Icon name="refresh" size={16} color="#2196F3" />
          <Text style={styles.retryText}>Retry</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  const renderLoading = () => (
    <View style={styles.loadingContainer}>
      <ActivityIndicator size="large" color="#2196F3" />
      <Text style={styles.loadingText}>Loading camera feed...</Text>
    </View>
  );

  const renderImage = () => (
    <View style={styles.imageContainer}>
      <Image
        source={{ uri: imageUrl }}
        style={styles.cameraImage}
        resizeMode="cover"
      />
      {lastUpdated && (
        <View style={styles.timestampContainer}>
          <Text style={styles.timestampText}>
            Last updated: {lastUpdated.toLocaleTimeString()}
          </Text>
        </View>
      )}
    </View>
  );

  const renderError = () => (
    <View style={styles.errorContainer}>
      <Icon name="error" size={40} color="#F44336" />
      <Text style={styles.errorText}>Failed to load camera feed</Text>
      <TouchableOpacity style={styles.retryButton} onPress={loadCameraFrame}>
        <Icon name="refresh" size={16} color="#2196F3" />
        <Text style={styles.retryText}>Retry</Text>
      </TouchableOpacity>
    </View>
  );

  if (loading) {
    return renderLoading();
  }

  if (error || !camera?.is_active) {
    return renderError();
  }

  if (!imageUrl) {
    return renderPlaceholder();
  }

  return renderImage();
};

const styles = StyleSheet.create({
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  placeholderText: {
    marginTop: 10,
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 14,
    color: '#FFFFFF',
  },
  imageContainer: {
    flex: 1,
    position: 'relative',
  },
  cameraImage: {
    width: '100%',
    height: '100%',
  },
  timestampContainer: {
    position: 'absolute',
    bottom: 10,
    right: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  timestampText: {
    fontSize: 10,
    color: '#FFFFFF',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFEBEE',
  },
  errorText: {
    marginTop: 10,
    fontSize: 14,
    color: '#D32F2F',
    textAlign: 'center',
    marginBottom: 15,
  },
  retryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E3F2FD',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#2196F3',
  },
  retryText: {
    marginLeft: 4,
    fontSize: 12,
    color: '#2196F3',
    fontWeight: '500',
  },
});

export default CameraFeed; 