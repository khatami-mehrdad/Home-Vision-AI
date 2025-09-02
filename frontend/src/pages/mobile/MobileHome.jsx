import React from 'react';
import { useNavigate } from 'react-router-dom';

const MobileHome = () => {
  const navigate = useNavigate();

  const stats = [
    { label: 'Active Cameras', value: '3', icon: '📹', color: 'bg-blue-500' },
    { label: 'Alerts Today', value: '5', icon: '🔔', color: 'bg-red-500' },
    { label: 'Events', value: '12', icon: '📊', color: 'bg-green-500' },
    { label: 'System Status', value: 'Online', icon: '🟢', color: 'bg-green-500' },
  ];

  const quickActions = [
    {
      title: 'View Cameras',
      description: 'Check live camera feeds',
      icon: '📹',
      path: '/cameras',
      color: 'bg-blue-500',
    },
    {
      title: 'Notifications',
      description: 'View recent alerts',
      icon: '🔔',
      path: '/notifications',
      color: 'bg-red-500',
    },
    {
      title: 'Settings',
      description: 'Configure system',
      icon: '⚙️',
      path: '/settings',
      color: 'bg-gray-500',
    },
  ];

  return (
    <div className="p-4 space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-6 text-white">
        <h2 className="text-2xl font-bold mb-2">Welcome back!</h2>
        <p className="text-blue-100">Your home security system is running smoothly</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.label}</p>
                <p className="text-xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`w-10 h-10 rounded-full ${stat.color} flex items-center justify-center text-white text-lg`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="space-y-3">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => navigate(action.path)}
              className="w-full bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center space-x-4 hover:shadow-md transition-shadow"
            >
              <div className={`w-12 h-12 rounded-xl ${action.color} flex items-center justify-center text-white text-xl`}>
                {action.icon}
              </div>
              <div className="flex-1 text-left">
                <h4 className="font-semibold text-gray-900">{action.title}</h4>
                <p className="text-sm text-gray-600">{action.description}</p>
              </div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-4 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-900">Camera 1 motion detected</span>
              <span className="text-xs text-gray-500 ml-auto">2 min ago</span>
            </div>
          </div>
          <div className="p-4 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-900">System backup completed</span>
              <span className="text-xs text-gray-500 ml-auto">15 min ago</span>
            </div>
          </div>
          <div className="p-4">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-900">Camera 2 connection restored</span>
              <span className="text-xs text-gray-500 ml-auto">1 hour ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileHome;

