import React, { useState } from 'react';
import { 
  Camera, 
  Plus, 
  Settings, 
  Edit3, 
  Trash2, 
  Power, 
  PowerOff,
  Wifi,
  WifiOff,
  CheckCircle,
  AlertTriangle,
  MoreVertical,
  Eye,
  EyeOff,
  Volume2,
  VolumeX
} from 'lucide-react';
import CameraGrid from '../components/camera/CameraGrid';

const Cameras = () => {
  const [viewMode, setViewMode] = useState('grid'); // grid, list
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedCamera, setSelectedCamera] = useState(null);

  // Mock camera data - replace with real API data
  const mockCameras = [
    {
      id: 1,
      name: 'Front Door',
      location: 'Entrance',
      url: 'rtsp://192.168.1.100:554/stream1',
      status: 'online',
      resolution: '1920x1080',
      frame_rate: 30,
      is_recording: true,
      last_seen: '2024-01-15T10:30:00Z',
      model: 'Hikvision DS-2CD2143G0-I',
      zone: 'entrance'
    },
    {
      id: 2,
      name: 'Backyard',
      location: 'Garden',
      url: 'rtsp://192.168.1.101:554/stream1',
      status: 'online',
      resolution: '1920x1080',
      frame_rate: 25,
      is_recording: false,
      last_seen: '2024-01-15T10:29:00Z',
      model: 'Dahua IPC-HFW2431S-S-S2',
      zone: 'garden'
    },
    {
      id: 3,
      name: 'Driveway',
      location: 'Parking',
      url: 'rtsp://192.168.1.102:554/stream1',
      status: 'offline',
      resolution: '1920x1080',
      frame_rate: 30,
      is_recording: false,
      last_seen: '2024-01-15T09:15:00Z',
      model: 'Axis M3027-PVE',
      zone: 'driveway'
    }
  ];

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
      default: return AlertTriangle;
    }
  };

  const formatLastSeen = (timestamp) => {
    const now = new Date();
    const lastSeen = new Date(timestamp);
    const diffInMinutes = Math.floor((now - lastSeen) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  return (
    <div className="h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-gray-700 pb-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-white">Camera Management</h1>
          <button 
            onClick={() => setShowAddModal(true)}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <Plus className="h-4 w-4" />
            <span>Add Camera</span>
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Total Cameras</p>
                <p className="text-2xl font-bold text-white">{mockCameras.length}</p>
              </div>
              <Camera className="h-8 w-8 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Online</p>
                <p className="text-2xl font-bold text-green-400">
                  {mockCameras.filter(c => c.status === 'online').length}
                </p>
              </div>
              <Wifi className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Recording</p>
                <p className="text-2xl font-bold text-red-400">
                  {mockCameras.filter(c => c.is_recording).length}
                </p>
              </div>
              <Eye className="h-8 w-8 text-red-500" />
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Offline</p>
                <p className="text-2xl font-bold text-red-400">
                  {mockCameras.filter(c => c.status === 'offline').length}
                </p>
              </div>
              <WifiOff className="h-8 w-8 text-red-500" />
            </div>
          </div>
        </div>

        {/* View Toggle */}
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-400">View:</span>
            <div className="flex items-center space-x-2 bg-gray-800 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-1 rounded text-sm transition-colors ${
                  viewMode === 'grid' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                Grid
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1 rounded text-sm transition-colors ${
                  viewMode === 'list' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                List
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Camera Display */}
      {viewMode === 'grid' ? (
        <CameraGrid />
      ) : (
        /* List View */
        <div className="space-y-4">
          {mockCameras.map((camera) => {
            const StatusIcon = getStatusIcon(camera.status);
            
            return (
              <div
                key={camera.id}
                className="bg-gray-800 rounded-lg border border-gray-700 hover:border-gray-600 transition-colors"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between">
                    {/* Camera Info */}
                    <div className="flex items-center space-x-4">
                      <div className="w-16 h-12 bg-gray-700 rounded-lg flex items-center justify-center">
                        <Camera className="h-6 w-6 text-gray-400" />
                      </div>
                      
                      <div>
                        <h3 className="font-semibold text-white text-lg">{camera.name}</h3>
                        <p className="text-gray-400 text-sm">{camera.location}</p>
                        <p className="text-gray-500 text-xs">{camera.model}</p>
                      </div>
                    </div>

                    {/* Status and Controls */}
                    <div className="flex items-center space-x-6">
                      {/* Status */}
                      <div className="text-center">
                        <div className="flex items-center justify-center space-x-2 mb-1">
                          <StatusIcon className={`h-4 w-4 ${getStatusColor(camera.status)}`} />
                          <span className={`text-sm font-medium capitalize ${getStatusColor(camera.status)}`}>
                            {camera.status}
                          </span>
                        </div>
                        <p className="text-xs text-gray-500">
                          {camera.status === 'online' ? 'Active now' : formatLastSeen(camera.last_seen)}
                        </p>
                      </div>

                      {/* Specs */}
                      <div className="text-center">
                        <p className="text-sm font-medium text-white">{camera.resolution}</p>
                        <p className="text-xs text-gray-400">{camera.frame_rate} FPS</p>
                      </div>

                      {/* Recording Status */}
                      <div className="text-center">
                        <div className="flex items-center justify-center space-x-1 mb-1">
                          {camera.is_recording ? (
                            <>
                              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                              <span className="text-sm text-red-400">Recording</span>
                            </>
                          ) : (
                            <span className="text-sm text-gray-400">Standby</span>
                          )}
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex items-center space-x-2">
                        <button 
                          className={`p-2 rounded-lg transition-colors ${
                            camera.status === 'online' 
                              ? 'bg-red-600 hover:bg-red-700 text-white' 
                              : 'bg-green-600 hover:bg-green-700 text-white'
                          }`}
                          title={camera.status === 'online' ? 'Stop Camera' : 'Start Camera'}
                        >
                          {camera.status === 'online' ? (
                            <PowerOff className="h-4 w-4" />
                          ) : (
                            <Power className="h-4 w-4" />
                          )}
                        </button>

                        <button 
                          className="p-2 bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white rounded-lg transition-colors"
                          title="Edit Camera"
                        >
                          <Edit3 className="h-4 w-4" />
                        </button>

                        <button 
                          className="p-2 bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white rounded-lg transition-colors"
                          title="Camera Settings"
                        >
                          <Settings className="h-4 w-4" />
                        </button>

                        <button 
                          className="p-2 bg-gray-700 hover:bg-red-600 text-gray-300 hover:text-white rounded-lg transition-colors"
                          title="Delete Camera"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>

                        <button 
                          className="p-2 bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white rounded-lg transition-colors"
                          title="More Options"
                        >
                          <MoreVertical className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Additional Details */}
                  <div className="mt-4 pt-4 border-t border-gray-700">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center space-x-6 text-gray-400">
                        <span>Zone: {camera.zone}</span>
                        <span>URL: {camera.url.substring(0, 30)}...</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button className="text-gray-400 hover:text-white transition-colors">
                          <Volume2 className="h-4 w-4" />
                        </button>
                        <button className="text-gray-400 hover:text-white transition-colors">
                          <Eye className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Add Camera Modal Placeholder */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-white mb-4">Add New Camera</h2>
            <p className="text-gray-400 mb-4">Camera configuration form would go here.</p>
            <div className="flex space-x-3">
              <button 
                onClick={() => setShowAddModal(false)}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button 
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition-colors"
              >
                Add Camera
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cameras;