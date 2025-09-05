import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RefreshCw } from 'lucide-react';

const CameraFeed = ({ camera }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const imgRef = useRef(null);
  const intervalRef = useRef(null);

  const startStream = () => {
    if (isPlaying) return;
    
    setIsLoading(true);
    setError(null);
    setIsPlaying(true);
    
    // Start polling for frames
    intervalRef.current = setInterval(() => {
      fetchFrame();
    }, 1000 / camera.frame_rate); // Update based on camera frame rate
  };

  const stopStream = () => {
    setIsPlaying(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const fetchFrame = async () => {
    try {
      const response = await fetch(`/api/v1/cameras/${camera.id}/frame`);
      if (!response.ok) {
        throw new Error('Failed to fetch frame');
      }
      
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      
      if (imgRef.current) {
        imgRef.current.src = url;
      }
      
      setIsLoading(false);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
      stopStream();
    }
  };

  const refreshStream = () => {
    stopStream();
    setTimeout(() => {
      startStream();
    }, 100);
  };

  useEffect(() => {
    // Auto-start stream if camera is online
    if (camera.status === 'online') {
      startStream();
    }

    return () => {
      stopStream();
    };
  }, [camera.id, camera.status]);

  if (camera.status === 'offline') {
    return (
      <div className="aspect-video bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-gray-300 rounded-full flex items-center justify-center mx-auto mb-4">
            <RefreshCw className="h-8 w-8 text-gray-500" />
          </div>
          <p className="text-sm text-gray-500">Camera Offline</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative aspect-video bg-black">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-10">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
        </div>
      )}
      
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-75 z-10">
          <div className="text-center text-white">
            <p className="text-sm mb-2">Stream Error</p>
            <button
              onClick={refreshStream}
              className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
      )}
      
      <img
        ref={imgRef}
        alt={`${camera.name} feed`}
        className="w-full h-full object-cover"
        onLoad={() => setIsLoading(false)}
        onError={() => {
          setError('Failed to load image');
          setIsLoading(false);
        }}
      />
      
      <div className="absolute bottom-2 right-2 flex space-x-2">
        {isPlaying ? (
          <button
            onClick={stopStream}
            className="p-2 bg-black bg-opacity-50 text-white rounded hover:bg-opacity-75"
            title="Pause Stream"
          >
            <Pause className="h-4 w-4" />
          </button>
        ) : (
          <button
            onClick={startStream}
            className="p-2 bg-black bg-opacity-50 text-white rounded hover:bg-opacity-75"
            title="Play Stream"
          >
            <Play className="h-4 w-4" />
          </button>
        )}

        <button
          onClick={refreshStream}
          className="p-2 bg-black bg-opacity-50 text-white rounded hover:bg-opacity-75"
          title="Refresh Stream"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

export default CameraFeed; 