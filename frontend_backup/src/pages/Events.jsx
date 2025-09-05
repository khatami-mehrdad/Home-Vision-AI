import React, { useState } from 'react';
import { 
  Calendar,
  Clock,
  Camera,
  Play,
  Download,
  Filter,
  Search,
  ChevronLeft,
  ChevronRight,
  AlertTriangle,
  CheckCircle,
  User,
  Car,
  Package,
  Eye
} from 'lucide-react';

const Events = () => {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedCamera, setSelectedCamera] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('timeline'); // timeline, grid

  // Mock data - replace with real API data
  const mockEvents = [
    {
      id: 1,
      timestamp: '2024-01-15T10:30:00Z',
      camera: 'Front Door',
      type: 'person',
      confidence: 0.95,
      thumbnail: '/api/placeholder/320/240',
      duration: 12,
      hasVideo: true,
      zone: 'entrance'
    },
    {
      id: 2,
      timestamp: '2024-01-15T10:25:00Z',
      camera: 'Backyard',
      type: 'cat',
      confidence: 0.88,
      thumbnail: '/api/placeholder/320/240',
      duration: 8,
      hasVideo: true,
      zone: 'garden'
    },
    {
      id: 3,
      timestamp: '2024-01-15T10:20:00Z',
      camera: 'Driveway',
      type: 'car',
      confidence: 0.92,
      thumbnail: '/api/placeholder/320/240',
      duration: 15,
      hasVideo: true,
      zone: 'driveway'
    },
  ];

  const getEventIcon = (type) => {
    switch (type) {
      case 'person': return User;
      case 'car': return Car;
      case 'cat': return Eye;
      case 'package': return Package;
      default: return AlertTriangle;
    }
  };

  const getEventColor = (type) => {
    switch (type) {
      case 'person': return 'text-blue-400';
      case 'car': return 'text-green-400';
      case 'cat': return 'text-purple-400';
      case 'package': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-gray-700 pb-6 mb-6">
        <h1 className="text-2xl font-bold text-white mb-4">Events</h1>
        
        {/* Filters */}
        <div className="flex flex-wrap items-center gap-4">
          {/* Date Picker */}
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-400" />
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Camera Filter */}
          <select
            value={selectedCamera}
            onChange={(e) => setSelectedCamera(e.target.value)}
            className="bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Cameras</option>
            <option value="front-door">Front Door</option>
            <option value="backyard">Backyard</option>
            <option value="driveway">Driveway</option>
          </select>

          {/* Type Filter */}
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option value="person">Person</option>
            <option value="car">Car</option>
            <option value="cat">Cat</option>
            <option value="package">Package</option>
          </select>

          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search events..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-gray-800 border border-gray-600 rounded-lg pl-10 pr-3 py-2 text-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* View Mode */}
          <div className="flex items-center space-x-2 bg-gray-800 rounded-lg p-1">
            <button
              onClick={() => setViewMode('timeline')}
              className={`px-3 py-1 rounded text-sm transition-colors ${
                viewMode === 'timeline' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              Timeline
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`px-3 py-1 rounded text-sm transition-colors ${
                viewMode === 'grid' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              Grid
            </button>
          </div>
        </div>
      </div>

      {/* Events Display */}
      {viewMode === 'timeline' ? (
        /* Timeline View */
        <div className="space-y-4">
          {mockEvents.map((event) => {
            const EventIcon = getEventIcon(event.type);
            
            return (
              <div
                key={event.id}
                className="bg-gray-800 rounded-lg border border-gray-700 hover:border-gray-600 transition-colors"
              >
                <div className="p-4">
                  <div className="flex items-start space-x-4">
                    {/* Thumbnail */}
                    <div className="relative">
                      <div className="w-32 h-24 bg-gray-700 rounded-lg overflow-hidden">
                        <img
                          src={event.thumbnail}
                          alt="Event thumbnail"
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjI0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzc0MTUxIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzlDQTNBRiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==';
                          }}
                        />
                      </div>
                      <button className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 hover:bg-opacity-70 transition-all rounded-lg">
                        <Play className="h-6 w-6 text-white" />
                      </button>
                    </div>

                    {/* Event Details */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <EventIcon className={`h-5 w-5 ${getEventColor(event.type)}`} />
                          <h3 className="font-medium text-white capitalize">{event.type} Detected</h3>
                          <span className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">
                            {Math.round(event.confidence * 100)}%
                          </span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <button className="text-gray-400 hover:text-white transition-colors">
                            <Download className="h-4 w-4" />
                          </button>
                        </div>
                      </div>

                      <div className="flex items-center space-x-4 text-sm text-gray-400 mb-2">
                        <div className="flex items-center space-x-1">
                          <Camera className="h-4 w-4" />
                          <span>{event.camera}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Clock className="h-4 w-4" />
                          <span>{formatTime(event.timestamp)}</span>
                        </div>
                        <span>Duration: {event.duration}s</span>
                        <span>Zone: {event.zone}</span>
                      </div>

                      <p className="text-sm text-gray-300">
                        Motion detected in the {event.zone} area with high confidence.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        /* Grid View */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {mockEvents.map((event) => {
            const EventIcon = getEventIcon(event.type);
            
            return (
              <div
                key={event.id}
                className="bg-gray-800 rounded-lg border border-gray-700 hover:border-gray-600 transition-colors overflow-hidden"
              >
                {/* Thumbnail */}
                <div className="relative aspect-video">
                  <img
                    src={event.thumbnail}
                    alt="Event thumbnail"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIwIiBoZWlnaHQ9IjI0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzc0MTUxIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzlDQTNBRiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==';
                    }}
                  />
                  <button className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 hover:bg-opacity-70 transition-all">
                    <Play className="h-8 w-8 text-white" />
                  </button>
                  
                  {/* Event Badge */}
                  <div className="absolute top-2 left-2 flex items-center space-x-1 bg-black bg-opacity-70 px-2 py-1 rounded text-xs">
                    <EventIcon className={`h-3 w-3 ${getEventColor(event.type)}`} />
                    <span className="text-white capitalize">{event.type}</span>
                  </div>
                  
                  {/* Confidence */}
                  <div className="absolute top-2 right-2 bg-black bg-opacity-70 px-2 py-1 rounded text-xs text-white">
                    {Math.round(event.confidence * 100)}%
                  </div>
                </div>

                {/* Event Info */}
                <div className="p-3">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-white truncate">{event.camera}</h3>
                    <span className="text-xs text-gray-400">{formatTime(event.timestamp)}</span>
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span>Zone: {event.zone}</span>
                    <span>{event.duration}s</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Pagination */}
      <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-700">
        <div className="text-sm text-gray-400">
          Showing {mockEvents.length} of {mockEvents.length} events
        </div>
        <div className="flex items-center space-x-2">
          <button className="flex items-center space-x-1 bg-gray-800 hover:bg-gray-700 border border-gray-600 px-3 py-2 rounded-lg text-sm transition-colors">
            <ChevronLeft className="h-4 w-4" />
            <span>Previous</span>
          </button>
          <button className="flex items-center space-x-1 bg-gray-800 hover:bg-gray-700 border border-gray-600 px-3 py-2 rounded-lg text-sm transition-colors">
            <span>Next</span>
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Events;