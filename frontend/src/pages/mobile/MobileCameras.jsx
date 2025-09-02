import React, { useState, useEffect } from 'react';

const MobileCameras = () => {
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [loadingStates, setLoadingStates] = useState({});

  // Auto-refresh camera feeds every 2 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setRefreshKey(prev => prev + 1);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleImageLoad = (cameraId) => {
    setLoadingStates(prev => ({ ...prev, [cameraId]: false }));
  };

  const handleImageError = (cameraId) => {
    setLoadingStates(prev => ({ ...prev, [cameraId]: false }));
  };

  const handleImageLoadStart = (cameraId) => {
    setLoadingStates(prev => ({ ...prev, [cameraId]: true }));
  };

  const cameras = [
    {
      id: 1,
      name: 'Front Door',
      status: 'online',
      location: 'Front Entrance',
      lastActivity: '2 min ago',
      streamUrl: 'http://localhost:8000/api/v1/cameras/1/frame',
    },
    {
      id: 2,
      name: 'Backyard',
      status: 'online',
      location: 'Back Garden',
      lastActivity: '5 min ago',
      streamUrl: 'http://localhost:8000/api/v1/cameras/2/frame',
    },
    {
      id: 3,
      name: 'Garage',
      status: 'offline',
      location: 'Garage',
      lastActivity: '1 hour ago',
      streamUrl: 'http://localhost:8000/api/v1/cameras/3/frame',
    },
  ];

  const getStatusColor = (status) => {
    return status === 'online' ? 'bg-green-500' : 'bg-red-500';
  };

  const getStatusText = (status) => {
    return status === 'online' ? 'Online' : 'Offline';
  };

  return (
    <div className="p-4 space-y-4">
      {/* Camera Grid */}
      <div className="grid grid-cols-1 gap-4">
        {cameras.map((camera) => (
          <div
            key={camera.id}
            className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
          >
            {/* Camera Header */}
            <div className="p-4 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900">{camera.name}</h3>
                  <p className="text-sm text-gray-600">{camera.location}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${getStatusColor(camera.status)}`}></div>
                  <span className="text-xs text-gray-600">{getStatusText(camera.status)}</span>
                </div>
              </div>
            </div>

            {/* Camera Feed */}
            <div className="relative">
              <div className="aspect-video bg-gray-100 flex items-center justify-center">
                {camera.status === 'online' ? (
                  <>
                    {loadingStates[camera.id] && (
                      <div className="absolute inset-0 flex items-center justify-center bg-gray-200 z-10">
                        <div className="text-center">
                          <svg className="animate-spin w-8 h-8 text-blue-500 mx-auto mb-2" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <p className="text-sm text-gray-600">Loading...</p>
                        </div>
                      </div>
                    )}
                    <img
                      src={`${camera.streamUrl}?t=${refreshKey}`}
                      alt={camera.name}
                      className="w-full h-full object-cover"
                      onLoadStart={() => handleImageLoadStart(camera.id)}
                      onLoad={() => handleImageLoad(camera.id)}
                      onError={() => handleImageError(camera.id)}
                    />
                  </>
                ) : null}
                <div className="absolute inset-0 flex items-center justify-center bg-gray-200">
                  <div className="text-center">
                    <svg className="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    <p className="text-sm text-gray-500">Camera Offline</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Camera Controls */}
            <div className="p-4">
              <div className="flex items-center justify-between">
                <div className="text-xs text-gray-500">
                  Last activity: {camera.lastActivity}
                </div>
                <div className="flex space-x-2">
                  <button className="px-3 py-1 text-xs bg-blue-500 text-white rounded-lg hover:bg-blue-600">
                    View Full
                  </button>
                  <button className="px-3 py-1 text-xs bg-gray-500 text-white rounded-lg hover:bg-gray-600">
                    Settings
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-3">Quick Actions</h3>
        <div className="grid grid-cols-2 gap-3">
          <button className="flex items-center justify-center space-x-2 p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-sm">Add Camera</span>
          </button>
          <button className="flex items-center justify-center space-x-2 p-3 bg-green-500 text-white rounded-lg hover:bg-green-600">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span className="text-sm">Refresh All</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default MobileCameras;
