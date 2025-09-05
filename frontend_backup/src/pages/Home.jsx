import React, { useState } from 'react';
import { useCamera } from '../context/CameraContext';
import { 
  Camera, 
  Play, 
  Maximize2, 
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react';
import CameraFeed from '../components/CameraFeed';

const Home = () => {
  const { cameras, loading } = useCamera();
  const [selectedCamera, setSelectedCamera] = useState(null);

  const getStatusColor = (status) => {
    switch (status) {
      case 'online': return 'text-green-400';
      case 'offline': return 'text-red-400';
      case 'warning': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'online': return CheckCircle;
      case 'offline': return AlertTriangle;
      case 'warning': return AlertTriangle;
      default: return Clock;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading cameras...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-900 text-white">
      {/* Camera Grid - Full Screen Focus */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-2 p-2">
        {cameras?.map((camera) => {
          const StatusIcon = getStatusIcon(camera.status);
          
          return (
            <div
              key={camera.id}
              className={`bg-gray-800 rounded overflow-hidden border-2 transition-all duration-200 cursor-pointer group ${
                selectedCamera?.id === camera.id
                  ? 'border-blue-500'
                  : 'border-gray-700 hover:border-gray-600'
              }`}
              onClick={() => setSelectedCamera(camera)}
            >
              {/* Camera Feed with Minimal Header */}
              <div className="relative aspect-video bg-gray-900">
                {/* Minimal Header Overlay */}
                <div className="absolute top-0 left-0 right-0 bg-gradient-to-b from-black/70 to-transparent p-2 z-10">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium text-white text-sm truncate">{camera.name}</h3>
                    <div className="flex items-center space-x-1">
                      {camera.is_recording && (
                        <div className="flex items-center space-x-1">
                          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                          <span className="text-xs text-red-400">REC</span>
                        </div>
                      )}
                      <StatusIcon className={`h-3 w-3 ${getStatusColor(camera.status)}`} />
                    </div>
                  </div>
                </div>

                {/* Camera Feed */}
                {camera.status === 'online' ? (
                  <CameraFeed
                    key={camera.id}
                    cameraId={camera.id}
                    cameraName={camera.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <Camera className="h-12 w-12 text-gray-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-500">Camera Offline</p>
                    </div>
                  </div>
                )}
                
                {/* Minimal Bottom Info */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2">
                  <div className="flex items-center justify-between text-xs text-gray-300">
                    <span className="capitalize">{camera.status}</span>
                    <span>{camera.frame_rate} FPS</span>
                  </div>
                </div>

                {/* Hover Controls */}
                <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <div className="flex space-x-2">
                    <button className="bg-black bg-opacity-60 hover:bg-opacity-80 text-white p-2 rounded-full transition-all">
                      <Play className="h-4 w-4" />
                    </button>
                    <button className="bg-black bg-opacity-60 hover:bg-opacity-80 text-white p-2 rounded-full transition-all">
                      <Maximize2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty State */}
      {(!cameras || cameras.length === 0) && (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <Camera className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-300 mb-2">
              No cameras configured
            </h3>
            <p className="text-gray-500 mb-4">
              Add cameras to start monitoring your home
            </p>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
              Add Camera
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;