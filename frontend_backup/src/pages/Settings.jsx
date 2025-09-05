import React, { useState } from 'react';
import { 
  Settings as SettingsIcon, 
  Camera, 
  Bell, 
  Shield, 
  Monitor, 
  Database,
  Wifi,
  Volume2,
  Moon,
  Sun,
  Globe,
  Save,
  RotateCcw,
  AlertTriangle,
  CheckCircle,
  Info
} from 'lucide-react';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    // General Settings
    systemName: 'Home Vision AI',
    timeZone: 'America/New_York',
    theme: 'dark',
    language: 'en',
    
    // Camera Settings
    defaultResolution: '1920x1080',
    defaultFrameRate: 30,
    recordingQuality: 'high',
    motionSensitivity: 75,
    
    // Detection Settings
    enablePersonDetection: true,
    enableCatDetection: true,
    enableCarDetection: false,
    confidenceThreshold: 80,
    
    // Notification Settings
    enableNotifications: true,
    notificationSound: true,
    emailNotifications: false,
    pushNotifications: true,
    
    // Storage Settings
    recordingRetention: 30,
    maxStorageSize: 100,
    autoCleanup: true,
    
    // Network Settings
    rtspPort: 554,
    webPort: 3000,
    apiPort: 8000,
    enableSSL: false
  });

  const tabs = [
    { id: 'general', label: 'General', icon: SettingsIcon },
    { id: 'cameras', label: 'Cameras', icon: Camera },
    { id: 'detection', label: 'AI Detection', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'storage', label: 'Storage', icon: Database },
    { id: 'network', label: 'Network', icon: Wifi }
  ];

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    // Save settings logic here
    console.log('Saving settings:', settings);
  };

  const handleReset = () => {
    // Reset to defaults logic here
    console.log('Resetting settings to defaults');
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  System Name
                </label>
                <input
                  type="text"
                  value={settings.systemName}
                  onChange={(e) => handleSettingChange('systemName', e.target.value)}
                  className="input w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Time Zone
                </label>
                <select
                  value={settings.timeZone}
                  onChange={(e) => handleSettingChange('timeZone', e.target.value)}
                  className="input w-full"
                >
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Theme
                </label>
                <select
                  value={settings.theme}
                  onChange={(e) => handleSettingChange('theme', e.target.value)}
                  className="input w-full"
                >
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                  <option value="auto">Auto</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Language
                </label>
                <select
                  value={settings.language}
                  onChange={(e) => handleSettingChange('language', e.target.value)}
                  className="input w-full"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                </select>
              </div>
            </div>
          </div>
        );
        
      case 'cameras':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Default Resolution
                </label>
                <select
                  value={settings.defaultResolution}
                  onChange={(e) => handleSettingChange('defaultResolution', e.target.value)}
                  className="input w-full"
                >
                  <option value="1920x1080">1920x1080 (Full HD)</option>
                  <option value="1280x720">1280x720 (HD)</option>
                  <option value="3840x2160">3840x2160 (4K)</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Default Frame Rate
                </label>
                <select
                  value={settings.defaultFrameRate}
                  onChange={(e) => handleSettingChange('defaultFrameRate', parseInt(e.target.value))}
                  className="input w-full"
                >
                  <option value={15}>15 FPS</option>
                  <option value={25}>25 FPS</option>
                  <option value={30}>30 FPS</option>
                  <option value={60}>60 FPS</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Recording Quality
                </label>
                <select
                  value={settings.recordingQuality}
                  onChange={(e) => handleSettingChange('recordingQuality', e.target.value)}
                  className="input w-full"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="ultra">Ultra</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Motion Sensitivity: {settings.motionSensitivity}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={settings.motionSensitivity}
                  onChange={(e) => handleSettingChange('motionSensitivity', parseInt(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                />
              </div>
            </div>
          </div>
        );
        
      case 'detection':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-white">Detection Types</h3>
                
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-gray-300">Person Detection</label>
                  <button
                    onClick={() => handleSettingChange('enablePersonDetection', !settings.enablePersonDetection)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      settings.enablePersonDetection ? 'bg-blue-600' : 'bg-gray-600'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.enablePersonDetection ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
                
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-gray-300">Cat Detection</label>
                  <button
                    onClick={() => handleSettingChange('enableCatDetection', !settings.enableCatDetection)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      settings.enableCatDetection ? 'bg-blue-600' : 'bg-gray-600'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.enableCatDetection ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
                
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-gray-300">Car Detection</label>
                  <button
                    onClick={() => handleSettingChange('enableCarDetection', !settings.enableCarDetection)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      settings.enableCarDetection ? 'bg-blue-600' : 'bg-gray-600'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        settings.enableCarDetection ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Confidence Threshold: {settings.confidenceThreshold}%
                </label>
                <input
                  type="range"
                  min="50"
                  max="95"
                  value={settings.confidenceThreshold}
                  onChange={(e) => handleSettingChange('confidenceThreshold', parseInt(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                />
                <p className="text-xs text-gray-400 mt-1">
                  Higher values reduce false positives but may miss some detections
                </p>
              </div>
            </div>
          </div>
        );
        
      case 'notifications':
        return (
          <div className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-300">Enable Notifications</label>
                <button
                  onClick={() => handleSettingChange('enableNotifications', !settings.enableNotifications)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.enableNotifications ? 'bg-blue-600' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.enableNotifications ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-300">Notification Sound</label>
                <button
                  onClick={() => handleSettingChange('notificationSound', !settings.notificationSound)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.notificationSound ? 'bg-blue-600' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.notificationSound ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-300">Push Notifications</label>
                <button
                  onClick={() => handleSettingChange('pushNotifications', !settings.pushNotifications)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.pushNotifications ? 'bg-blue-600' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.pushNotifications ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-gray-300">Email Notifications</label>
                <button
                  onClick={() => handleSettingChange('emailNotifications', !settings.emailNotifications)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    settings.emailNotifications ? 'bg-blue-600' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      settings.emailNotifications ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>
        );
        
      case 'storage':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Recording Retention (days)
                </label>
                <input
                  type="number"
                  min="1"
                  max="365"
                  value={settings.recordingRetention}
                  onChange={(e) => handleSettingChange('recordingRetention', parseInt(e.target.value))}
                  className="input w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Max Storage Size (GB)
                </label>
                <input
                  type="number"
                  min="10"
                  max="1000"
                  value={settings.maxStorageSize}
                  onChange={(e) => handleSettingChange('maxStorageSize', parseInt(e.target.value))}
                  className="input w-full"
                />
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-300">Auto Cleanup Old Files</label>
              <button
                onClick={() => handleSettingChange('autoCleanup', !settings.autoCleanup)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.autoCleanup ? 'bg-blue-600' : 'bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.autoCleanup ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        );
        
      case 'network':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  RTSP Port
                </label>
                <input
                  type="number"
                  min="1"
                  max="65535"
                  value={settings.rtspPort}
                  onChange={(e) => handleSettingChange('rtspPort', parseInt(e.target.value))}
                  className="input w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Web Interface Port
                </label>
                <input
                  type="number"
                  min="1"
                  max="65535"
                  value={settings.webPort}
                  onChange={(e) => handleSettingChange('webPort', parseInt(e.target.value))}
                  className="input w-full"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  API Port
                </label>
                <input
                  type="number"
                  min="1"
                  max="65535"
                  value={settings.apiPort}
                  onChange={(e) => handleSettingChange('apiPort', parseInt(e.target.value))}
                  className="input w-full"
                />
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-300">Enable SSL/HTTPS</label>
              <button
                onClick={() => handleSettingChange('enableSSL', !settings.enableSSL)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  settings.enableSSL ? 'bg-blue-600' : 'bg-gray-600'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    settings.enableSSL ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-gray-700 pb-6 mb-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white">System Settings</h1>
          <div className="flex space-x-3">
            <button
              onClick={handleReset}
              className="btn-secondary flex items-center space-x-2"
            >
              <RotateCcw className="h-4 w-4" />
              <span>Reset</span>
            </button>
            <button
              onClick={handleSave}
              className="btn-primary flex items-center space-x-2"
            >
              <Save className="h-4 w-4" />
              <span>Save Changes</span>
            </button>
          </div>
        </div>
      </div>

      <div className="flex h-full">
        {/* Sidebar Tabs */}
        <div className="w-64 pr-6">
          <nav className="space-y-1">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <IconComponent className="h-5 w-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Content Area */}
        <div className="flex-1 bg-gray-800 rounded-lg border border-gray-700 p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white mb-2">
              {tabs.find(t => t.id === activeTab)?.label} Settings
            </h2>
            <p className="text-gray-400 text-sm">
              Configure your {tabs.find(t => t.id === activeTab)?.label.toLowerCase()} preferences
            </p>
          </div>
          
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default Settings;