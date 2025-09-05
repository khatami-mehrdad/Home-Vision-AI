import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { 
  Camera, 
  Video, 
  AlertCircle, 
  Play,
  Pause,
  Volume2,
  VolumeX,
  Maximize2,
  Settings,
  MoreVertical,
  CheckCircle,
  Clock,
  Wifi,
  WifiOff
} from 'lucide-react';
import { getCameras } from '../../services/api';
import CameraFeed from './CameraFeed';

const CameraGrid = () => {
  const { data: cameras, isLoading, error } = useQuery('cameras', getCameras);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // grid, single, split

  const getStatusColor = (status) => {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'offline': return 'bg-red-500';
      case 'warning': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'online': return CheckCircle;
      case 'offline': return WifiOff;
      case 'warning': return AlertCircle;
      default: return Clock;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading cameras...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-300 mb-2">
            Error loading cameras
          </h3>
          <p className="text-gray-500">
            {error.message || 'Failed to load camera feeds'}
          </p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!cameras || cameras.length === 0) {
    return (
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
    );
  }

  return (
    <div className="space-y-6">
      {/* View Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-semibold text-white">Camera Feeds</h2>
          <div className="flex items-center space-x-2 text-sm text-gray-400">
            <Wifi className="h-4 w-4 text-green-500" />
            <span>{cameras.filter(c => c.status === 'online').length} online</span>
            <span>•</span>
            <span>{cameras.length} total</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <select 
            value={viewMode} 
            onChange={(e) => setViewMode(e.target.value)}
            className="bg-gray-700 text-white border border-gray-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="grid">Grid View</option>
            <option value="single">Single View</option>
            <option value="split">Split View</option>
          </select>
        </div>
      </div>

      {/* Camera Grid */}
      <div className={`grid gap-4 ${
        viewMode === 'single' ? 'grid-cols-1' :
        viewMode === 'split' ? 'grid-cols-2' :
        'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
      }`}>
        {cameras.map((camera) => {
          const StatusIcon = getStatusIcon(camera.status);
          
          return (
            <div
              key={camera.id}
              className={`bg-gray-800 rounded-lg overflow-hidden border border-gray-700 hover:border-gray-600 transition-all duration-200 group ${
                selectedCamera?.id === camera.id ? 'ring-2 ring-blue-500' : ''
              }`}
              onClick={() => setSelectedCamera(camera)}
            >
              {/* Camera Header */}
              <div className="p-3 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 min-w-0 flex-1">
                    <h3 className="font-medium text-white truncate">{camera.name}</h3>
                    <div className="flex items-center space-x-1">
                      <div className={`w-2 h-2 rounded-full ${getStatusColor(camera.status)}`}></div>
                      <span className="text-xs text-gray-400 capitalize">{camera.status}</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {camera.is_recording && (
                      <div className="flex items-center space-x-1 bg-red-900 bg-opacity-50 px-2 py-1 rounded text-xs">
                        <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                        <Video className="h-3 w-3 text-red-400" />
                        <span className="text-red-400">REC</span>
                      </div>
                    )}
                    <button className="text-gray-400 hover:text-white transition-colors opacity-0 group-hover:opacity-100">
                      <MoreVertical className="h-4 w-4" />
                    </button>
                  </div>
                </div>
                
                <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
                  <span>{camera.location}</span>
                  <div className="flex items-center space-x-2">
                    <span>{camera.resolution}</span>
                    <span>•</span>
                    <span>{camera.frame_rate} FPS</span>
                  </div>
                </div>
              </div>

              {/* Camera Feed */}
              <div className="relative aspect-video bg-gray-900">
                {camera.status === 'online' ? (
                  <CameraFeed
                    camera={camera}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <StatusIcon className={`h-12 w-12 mx-auto mb-2 ${
                        camera.status === 'offline' ? 'text-red-500' : 'text-yellow-500'
                      }`} />
                      <p className="text-sm text-gray-500">
                        {camera.status === 'offline' ? 'Camera Offline' : 'Connection Issues'}
                      </p>
                    </div>
                  </div>
                )}
                
                {/* Overlay Controls */}
                <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <div className="flex space-x-2">
                    <button className="bg-black bg-opacity-60 hover:bg-opacity-80 text-white p-2 rounded-full transition-all">
                      <Play className="h-4 w-4" />
                    </button>
                    <button className="bg-black bg-opacity-60 hover:bg-opacity-80 text-white p-2 rounded-full transition-all">
                      <Volume2 className="h-4 w-4" />
                    </button>
                    <button className="bg-black bg-opacity-60 hover:bg-opacity-80 text-white p-2 rounded-full transition-all">
                      <Maximize2 className="h-4 w-4" />
                    </button>
                    <button className="bg-black bg-opacity-60 hover:bg-opacity-80 text-white p-2 rounded-full transition-all">
                      <Settings className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {/* Detection Overlay */}
                {camera.last_detection && (
                  <div className="absolute top-2 left-2 bg-blue-600 bg-opacity-90 text-white px-2 py-1 rounded text-xs">
                    Last: {camera.last_detection}
                  </div>
                )}
              </div>

              {/* Camera Footer */}
              <div className="p-3 bg-gray-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 text-xs text-gray-400">
                    <div className="flex items-center space-x-1">
                      <StatusIcon className="h-3 w-3" />
                      <span>Live</span>
                    </div>
                    <span>•</span>
                    <span>0ms delay</span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-xs text-green-400">Streaming</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CameraGrid;