import React, { useState, useEffect, useRef } from 'react';

const CameraFeed = ({ cameraId, cameraName }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [cameraStatus, setCameraStatus] = useState(null);
  const imgRef = useRef(null);
  const intervalRef = useRef(null);
  const statusIntervalRef = useRef(null);

  const fetchCameraStatus = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/cameras/${cameraId}/status`);
      if (response.ok) {
        const status = await response.json();
        setCameraStatus(status);
      }
    } catch (err) {
      console.error('Error fetching camera status:', err);
    }
  };

  const startCameraStream = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/cameras/${cameraId}/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        console.warn(`Failed to start camera stream: ${response.status}`);
      } else {
        console.log('Camera stream started successfully');
      }
    } catch (err) {
      console.error('Error starting camera stream:', err);
    }
  };

  const startStream = () => {
    if (isPlaying) return;
    
    setIsLoading(true);
    setError(null);
    setIsPlaying(true);
    
    // Start the camera stream first
    startCameraStream();
    
    // Start polling for frames
    intervalRef.current = setInterval(() => {
      fetchFrame();
    }, 1000 / 10); // 10 FPS
    
    // Start polling for camera status (every 2 seconds)
    statusIntervalRef.current = setInterval(() => {
      fetchCameraStatus();
    }, 2000);
  };

  const stopStream = () => {
    setIsPlaying(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (statusIntervalRef.current) {
      clearInterval(statusIntervalRef.current);
      statusIntervalRef.current = null;
    }
  };

  const fetchFrame = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/cameras/${cameraId}/frame`, {
        method: 'GET',
        headers: {
          'Accept': 'image/jpeg',
          'Cache-Control': 'no-cache'
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch frame: ${response.status}`);
      }
      
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      
      if (imgRef.current) {
        imgRef.current.src = url;
      }
      
      setIsLoading(false);
    } catch (err) {
      console.error('Frame fetch error:', err);
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
    // Auto-start stream
    startStream();

    return () => {
      stopStream();
    };
  }, [cameraId]);

  return (
    <div className="bg-white rounded-lg shadow-lg p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">{cameraName}</h3>
        <div className="flex space-x-2">
          <button
            onClick={isPlaying ? stopStream : startStream}
            className={`px-3 py-1 rounded text-sm ${
              isPlaying 
                ? 'bg-red-500 hover:bg-red-600 text-white' 
                : 'bg-green-500 hover:bg-green-600 text-white'
            }`}
          >
            {isPlaying ? 'Stop' : 'Start'}
          </button>
          <button
            onClick={refreshStream}
            className="px-3 py-1 rounded text-sm bg-blue-500 hover:bg-blue-600 text-white"
          >
            Refresh
          </button>
        </div>
      </div>
      
      <div className="relative bg-gray-900 rounded-lg overflow-hidden">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75">
            <div className="text-white">Loading...</div>
          </div>
        )}
        
        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75">
            <div className="text-red-400 text-center">
              <div>Error: {error}</div>
              <button
                onClick={refreshStream}
                className="mt-2 px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-sm"
              >
                Retry
              </button>
            </div>
          </div>
        )}
        
        <img
          ref={imgRef}
          alt={`${cameraName} feed`}
          className="w-full h-64 object-cover"
          style={{ display: error ? 'none' : 'block' }}
        />
      </div>
      
      <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-600">Status</div>
          <div className={`font-medium ${error ? 'text-red-600' : (isPlaying ? 'text-green-600' : 'text-gray-600')}`}>
            {error ? 'Error' : (isPlaying ? 'Streaming' : 'Stopped')}
          </div>
        </div>
        
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-600">AI FPS</div>
          <div className="font-medium text-blue-600">
            {cameraStatus?.current_fps || '0.00'} fps
          </div>
        </div>
        
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-600">Frames</div>
          <div className="font-medium">
            {cameraStatus?.frame_count || 0}
          </div>
        </div>
        
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-600">Detections</div>
          <div className="font-medium text-orange-600">
            {cameraStatus?.detections_count || 0}
          </div>
        </div>
        
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-600">Total Latency</div>
          <div className="font-medium text-purple-600">
            {cameraStatus?.avg_latency_ms || '0.0'} ms
          </div>
        </div>
        
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-600">Uptime</div>
          <div className="font-medium">
            {cameraStatus?.uptime_seconds ? `${Math.floor(cameraStatus.uptime_seconds / 60)}m ${cameraStatus.uptime_seconds % 60}s` : '0s'}
          </div>
        </div>
      </div>
      
      {/* Detailed Latency Breakdown */}
      {cameraStatus?.latency_breakdown && (
        <div className="mt-3">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Latency Breakdown</h4>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-blue-50 p-2 rounded">
              <div className="text-gray-600">RTSP Read</div>
              <div className="font-medium text-blue-600">
                {cameraStatus.latency_breakdown.rtsp_read_ms || '0.0'} ms
              </div>
            </div>
            
            <div className="bg-green-50 p-2 rounded">
              <div className="text-gray-600">AI Processing</div>
              <div className="font-medium text-green-600">
                {cameraStatus.latency_breakdown.ai_processing_ms || '0.0'} ms
              </div>
            </div>
            
            <div className="bg-yellow-50 p-2 rounded">
              <div className="text-gray-600">Frame Interval</div>
              <div className="font-medium text-yellow-600">
                {cameraStatus.latency_breakdown.frame_interval_ms || '0.0'} ms
              </div>
            </div>
            
            <div className="bg-indigo-50 p-2 rounded">
              <div className="text-gray-600">Camera FPS</div>
              <div className="font-medium text-indigo-600">
                {cameraStatus.latency_breakdown.actual_camera_fps || '0.0'} fps
              </div>
            </div>
          </div>
          
          <div className="mt-2 p-2 bg-red-50 rounded text-xs">
            <div className="text-gray-600">4-Second Delay Analysis</div>
            <div className="text-red-600 font-medium">
              Processing: {cameraStatus.avg_latency_ms || '0'}ms + Camera Buffer: ~{4000 - (cameraStatus.avg_latency_ms || 0)}ms
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CameraFeed; 