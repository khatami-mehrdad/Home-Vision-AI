import React from 'react';
import { useCamera } from '../context/CameraContext';
import CameraFeed from '../components/CameraFeed';

const Home = () => {
  const { cameras, loading } = useCamera();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      {loading ? (
        <p>Loading cameras...</p>
      ) : (
        <div className="space-y-6">
          {/* Camera Feeds */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Live Camera Feeds</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cameras.map(camera => (
                <CameraFeed
                  key={camera.id}
                  cameraId={camera.id}
                  cameraName={camera.name}
                />
              ))}
            </div>
          </div>

          {/* Camera Status Cards */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Camera Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cameras.map(camera => (
            <div key={camera.id} className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold">{camera.name}</h3>
              <p className="text-gray-600">{camera.location}</p>
              <p className={`text-sm ${camera.status === 'online' ? 'text-green-600' : 'text-red-600'}`}>
                Status: {camera.status}
              </p>
                  <p className="text-sm text-gray-500">Resolution: {camera.resolution}</p>
                  <p className="text-sm text-gray-500">Frame Rate: {camera.frame_rate} FPS</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
