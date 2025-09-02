import React, { useState } from 'react';

const MobileSettings = () => {
  const [settings, setSettings] = useState({
    notifications: {
      motion: true,
      system: true,
      info: false,
    },
    camera: {
      autoRecord: true,
      quality: 'high',
      retention: '7',
    },
    system: {
      autoBackup: true,
      darkMode: false,
    },
  });

  const handleToggle = (category, setting) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: !prev[category][setting],
      },
    }));
  };

  const handleSelect = (category, setting, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: value,
      },
    }));
  };

  return (
    <div className="p-4 space-y-6">
      {/* Profile Section */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-4">Profile</h3>
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
            JD
          </div>
          <div className="flex-1">
            <h4 className="font-semibold text-gray-900">John Doe</h4>
            <p className="text-sm text-gray-600">john.doe@example.com</p>
            <p className="text-xs text-gray-500">Admin</p>
          </div>
          <button className="px-3 py-1 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600">
            Edit
          </button>
        </div>
      </div>

      {/* Notification Settings */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-4">Notifications</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Motion Alerts</p>
              <p className="text-sm text-gray-600">Get notified when motion is detected</p>
            </div>
            <button
              onClick={() => handleToggle('notifications', 'motion')}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.notifications.motion ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                settings.notifications.motion ? 'transform translate-x-6' : 'transform translate-x-1'
              }`} />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">System Alerts</p>
              <p className="text-sm text-gray-600">Camera offline, connection issues</p>
            </div>
            <button
              onClick={() => handleToggle('notifications', 'system')}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.notifications.system ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                settings.notifications.system ? 'transform translate-x-6' : 'transform translate-x-1'
              }`} />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Info Notifications</p>
              <p className="text-sm text-gray-600">Backup completed, new devices</p>
            </div>
            <button
              onClick={() => handleToggle('notifications', 'info')}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.notifications.info ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                settings.notifications.info ? 'transform translate-x-6' : 'transform translate-x-1'
              }`} />
            </button>
          </div>
        </div>
      </div>

      {/* Camera Settings */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-4">Camera Settings</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Auto Record</p>
              <p className="text-sm text-gray-600">Automatically record on motion</p>
            </div>
            <button
              onClick={() => handleToggle('camera', 'autoRecord')}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.camera.autoRecord ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                settings.camera.autoRecord ? 'transform translate-x-6' : 'transform translate-x-1'
              }`} />
            </button>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">Video Quality</label>
            <select
              value={settings.camera.quality}
              onChange={(e) => handleSelect('camera', 'quality', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="low">Low (720p)</option>
              <option value="medium">Medium (1080p)</option>
              <option value="high">High (4K)</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">Retention (Days)</label>
            <select
              value={settings.camera.retention}
              onChange={(e) => handleSelect('camera', 'retention', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="1">1 day</option>
              <option value="7">7 days</option>
              <option value="30">30 days</option>
              <option value="90">90 days</option>
            </select>
          </div>
        </div>
      </div>

      {/* System Settings */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-4">System</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Auto Backup</p>
              <p className="text-sm text-gray-600">Daily system backup</p>
            </div>
            <button
              onClick={() => handleToggle('system', 'autoBackup')}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.system.autoBackup ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                settings.system.autoBackup ? 'transform translate-x-6' : 'transform translate-x-1'
              }`} />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900">Dark Mode</p>
              <p className="text-sm text-gray-600">Use dark theme</p>
            </div>
            <button
              onClick={() => handleToggle('system', 'darkMode')}
              className={`w-12 h-6 rounded-full transition-colors ${
                settings.system.darkMode ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                settings.system.darkMode ? 'transform translate-x-6' : 'transform translate-x-1'
              }`} />
            </button>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="space-y-3">
        <button className="w-full p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-medium">
          Save Settings
        </button>
        <button className="w-full p-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 font-medium">
          Logout
        </button>
      </div>
    </div>
  );
};

export default MobileSettings;
