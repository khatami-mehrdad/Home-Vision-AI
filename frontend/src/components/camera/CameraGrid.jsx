import React from 'react';
import { useQuery } from 'react-query';
import { Camera, Video, AlertCircle } from 'lucide-react';
import { getCameras } from '../../services/api';
import CameraFeed from './CameraFeed';
import Loading from '../common/Loading';

const CameraGrid = () => {
  const { data: cameras, isLoading, error } = useQuery('cameras', getCameras);

  if (isLoading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Error loading cameras
          </h3>
          <p className="text-gray-500">
            {error.message || 'Failed to load camera feeds'}
          </p>
        </div>
      </div>
    );
  }

  if (!cameras || cameras.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Camera className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No cameras configured
          </h3>
          <p className="text-gray-500">
            Add cameras to start monitoring your home
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {cameras.map((camera) => (
        <div
          key={camera.id}
          className="bg-white rounded-lg shadow-md overflow-hidden"
        >
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {camera.name}
                </h3>
                <p className="text-sm text-gray-500">{camera.location}</p>
              </div>
              <div className="flex items-center space-x-2">
                <div
                  className={`w-3 h-3 rounded-full ${
                    camera.status === 'online'
                      ? 'bg-green-500'
                      : camera.status === 'offline'
                      ? 'bg-red-500'
                      : 'bg-yellow-500'
                  }`}
                />
                <span className="text-sm text-gray-500 capitalize">
                  {camera.status}
                </span>
              </div>
            </div>
          </div>
          <div className="relative">
            <CameraFeed camera={camera} />
            {camera.is_recording && (
              <div className="absolute top-2 right-2">
                <div className="flex items-center space-x-1 bg-red-500 text-white px-2 py-1 rounded text-xs">
                  <Video className="h-3 w-3" />
                  <span>REC</span>
                </div>
              </div>
            )}
          </div>
          <div className="p-4">
            <div className="flex items-center justify-between text-sm text-gray-500">
              <span>{camera.resolution}</span>
              <span>{camera.frame_rate} FPS</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CameraGrid; 