import React, { useState } from 'react';
import { 
  Bell, 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  X,
  Filter,
  Search,
  Clock,
  Camera,
  User,
  Car,
  Eye,
  Trash2,
  MarkAsRead,
  Settings
} from 'lucide-react';

const Notifications = () => {
  const [filter, setFilter] = useState('all'); // all, unread, alerts, info
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNotifications, setSelectedNotifications] = useState([]);

  // Mock notification data
  const mockNotifications = [
    {
      id: 1,
      type: 'alert',
      category: 'person',
      title: 'Person Detected',
      message: 'Person detected at Front Door camera',
      camera: 'Front Door',
      timestamp: '2024-01-15T10:30:00Z',
      read: false,
      priority: 'high'
    },
    {
      id: 2,
      type: 'info',
      category: 'system',
      title: 'Camera Online',
      message: 'Backyard camera has come back online',
      camera: 'Backyard',
      timestamp: '2024-01-15T10:25:00Z',
      read: false,
      priority: 'medium'
    },
    {
      id: 3,
      type: 'alert',
      category: 'cat',
      title: 'Cat Detected',
      message: 'Cat detected in the garden area',
      camera: 'Backyard',
      timestamp: '2024-01-15T10:20:00Z',
      read: true,
      priority: 'medium'
    },
    {
      id: 4,
      type: 'warning',
      category: 'system',
      title: 'Storage Warning',
      message: 'Storage is 85% full. Consider cleaning up old recordings.',
      timestamp: '2024-01-15T09:15:00Z',
      read: true,
      priority: 'high'
    },
    {
      id: 5,
      type: 'alert',
      category: 'car',
      title: 'Vehicle Detected',
      message: 'Vehicle detected in driveway',
      camera: 'Driveway',
      timestamp: '2024-01-15T08:45:00Z',
      read: true,
      priority: 'low'
    }
  ];

  const getNotificationIcon = (type, category) => {
    if (category === 'person') return User;
    if (category === 'cat') return Eye;
    if (category === 'car') return Car;
    if (category === 'system') {
      switch (type) {
        case 'alert': return AlertTriangle;
        case 'warning': return AlertTriangle;
        case 'info': return Info;
        default: return Bell;
      }
    }
    return Bell;
  };

  const getNotificationColor = (type, priority) => {
    if (priority === 'high') return 'text-red-400';
    if (type === 'warning') return 'text-yellow-400';
    if (type === 'info') return 'text-blue-400';
    return 'text-gray-400';
  };

  const getNotificationBgColor = (type, priority, read) => {
    const baseClass = read ? 'bg-gray-800' : 'bg-gray-750';
    if (priority === 'high' && !read) return `${baseClass} border-l-4 border-red-500`;
    if (type === 'warning' && !read) return `${baseClass} border-l-4 border-yellow-500`;
    return baseClass;
  };

  const formatTime = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now - time) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const filteredNotifications = mockNotifications.filter(notification => {
    const matchesFilter = filter === 'all' || 
      (filter === 'unread' && !notification.read) ||
      (filter === 'alerts' && notification.type === 'alert') ||
      (filter === 'info' && notification.type === 'info');
    
    const matchesSearch = searchTerm === '' ||
      notification.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      notification.message.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesFilter && matchesSearch;
  });

  const unreadCount = mockNotifications.filter(n => !n.read).length;

  const handleSelectNotification = (id) => {
    setSelectedNotifications(prev => 
      prev.includes(id) 
        ? prev.filter(nId => nId !== id)
        : [...prev, id]
    );
  };

  const handleMarkAsRead = (ids) => {
    // Mark notifications as read logic
    console.log('Marking as read:', ids);
  };

  const handleDelete = (ids) => {
    // Delete notifications logic
    console.log('Deleting notifications:', ids);
  };

  return (
    <div className="h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-gray-700 pb-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-white">Notifications</h1>
            {unreadCount > 0 && (
              <span className="bg-red-600 text-white text-xs font-medium px-2 py-1 rounded-full">
                {unreadCount} new
              </span>
            )}
          </div>
          
          <div className="flex items-center space-x-3">
            {selectedNotifications.length > 0 && (
              <>
                <button
                  onClick={() => handleMarkAsRead(selectedNotifications)}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <CheckCircle className="h-4 w-4" />
                  <span>Mark Read</span>
                </button>
                <button
                  onClick={() => handleDelete(selectedNotifications)}
                  className="btn-danger flex items-center space-x-2"
                >
                  <Trash2 className="h-4 w-4" />
                  <span>Delete</span>
                </button>
              </>
            )}
            <button className="btn-secondary flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Settings</span>
            </button>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-wrap items-center gap-4">
          {/* Filter Buttons */}
          <div className="flex items-center space-x-2 bg-gray-800 rounded-lg p-1">
            {[
              { id: 'all', label: 'All' },
              { id: 'unread', label: 'Unread' },
              { id: 'alerts', label: 'Alerts' },
              { id: 'info', label: 'Info' }
            ].map((filterOption) => (
              <button
                key={filterOption.id}
                onClick={() => setFilter(filterOption.id)}
                className={`px-3 py-1 rounded text-sm transition-colors ${
                  filter === filterOption.id 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {filterOption.label}
                {filterOption.id === 'unread' && unreadCount > 0 && (
                  <span className="ml-1 text-xs">({unreadCount})</span>
                )}
              </button>
            ))}
          </div>

          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search notifications..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full input pl-10"
            />
          </div>
        </div>
      </div>

      {/* Notifications List */}
      <div className="space-y-3">
        {filteredNotifications.length === 0 ? (
          <div className="text-center py-12">
            <Bell className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-300 mb-2">
              No notifications found
            </h3>
            <p className="text-gray-500">
              {searchTerm ? 'Try adjusting your search terms' : 'All caught up!'}
            </p>
          </div>
        ) : (
          filteredNotifications.map((notification) => {
            const IconComponent = getNotificationIcon(notification.type, notification.category);
            const isSelected = selectedNotifications.includes(notification.id);
            
            return (
              <div
                key={notification.id}
                className={`${getNotificationBgColor(notification.type, notification.priority, notification.read)} 
                  rounded-lg border border-gray-700 hover:border-gray-600 transition-colors p-4 ${
                  isSelected ? 'ring-2 ring-blue-500' : ''
                }`}
              >
                <div className="flex items-start space-x-4">
                  {/* Checkbox */}
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => handleSelectNotification(notification.id)}
                    className="mt-1 h-4 w-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                  />

                  {/* Icon */}
                  <div className={`flex-shrink-0 p-2 rounded-lg ${
                    notification.priority === 'high' ? 'bg-red-900 bg-opacity-50' :
                    notification.type === 'warning' ? 'bg-yellow-900 bg-opacity-50' :
                    notification.type === 'info' ? 'bg-blue-900 bg-opacity-50' :
                    'bg-gray-700'
                  }`}>
                    <IconComponent className={`h-5 w-5 ${getNotificationColor(notification.type, notification.priority)}`} />
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <h3 className={`font-medium ${notification.read ? 'text-gray-300' : 'text-white'}`}>
                        {notification.title}
                      </h3>
                      <div className="flex items-center space-x-2 text-xs text-gray-400">
                        {notification.camera && (
                          <>
                            <Camera className="h-3 w-3" />
                            <span>{notification.camera}</span>
                            <span>•</span>
                          </>
                        )}
                        <Clock className="h-3 w-3" />
                        <span>{formatTime(notification.timestamp)}</span>
                      </div>
                    </div>
                    
                    <p className={`text-sm ${notification.read ? 'text-gray-400' : 'text-gray-300'}`}>
                      {notification.message}
                    </p>
                    
                    {/* Priority Badge */}
                    {notification.priority === 'high' && (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-900 bg-opacity-50 text-red-400 mt-2">
                        High Priority
                      </span>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    {!notification.read && (
                      <button
                        onClick={() => handleMarkAsRead([notification.id])}
                        className="p-1 text-gray-400 hover:text-blue-400 transition-colors"
                        title="Mark as read"
                      >
                        <CheckCircle className="h-4 w-4" />
                      </button>
                    )}
                    <button
                      onClick={() => handleDelete([notification.id])}
                      className="p-1 text-gray-400 hover:text-red-400 transition-colors"
                      title="Delete"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Pagination */}
      {filteredNotifications.length > 0 && (
        <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-700">
          <div className="text-sm text-gray-400">
            Showing {filteredNotifications.length} of {mockNotifications.length} notifications
          </div>
          <div className="text-sm text-gray-400">
            {selectedNotifications.length > 0 && (
              <span>{selectedNotifications.length} selected</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Notifications;