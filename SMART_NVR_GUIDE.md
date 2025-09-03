# Smart NVR Setup Guide

Your Home-Vision-AI system now includes advanced Smart NVR capabilities based on DeGirum's [Smart NVR example](https://github.com/DeGirum/PySDKExamples/blob/main/examples/applications/smart_nvr.ipynb). This transforms your basic camera system into a professional-grade Network Video Recorder with AI-powered analytics.

## 🚀 New Smart NVR Features

### 1. **Object Tracking**
- **Multi-Object Tracking**: Track people, vehicles, and objects across frames
- **Persistent IDs**: Objects maintain unique IDs throughout their journey
- **Path Recording**: Track movement paths and trajectories
- **Track Statistics**: Duration, first/last seen timestamps

### 2. **Detection Zones**
- **Virtual Boundaries**: Create rectangular or polygon detection zones
- **Restricted Areas**: Mark zones as restricted for security alerts
- **Zone Violations**: Automatic alerts when objects enter restricted zones
- **Multiple Zones**: Support for multiple zones per camera

### 3. **Smart Event Recording**
- **Event Types**:
  - `object_detected`: New object confirmed in view
  - `zone_violation`: Object entered restricted zone
  - `loitering_detected`: Object stayed too long (30+ seconds)
- **Event History**: Persistent storage of all events per camera
- **Alert Cooldowns**: Prevent spam notifications (30-second cooldown)

### 4. **Enhanced Analytics**
- **Real-time Statistics**: Active tracks, zones, events per camera
- **System Overview**: Total cameras, tracks, zones across all cameras
- **Performance Metrics**: Track confidence, detection accuracy

## 🔧 API Endpoints

### Object Detection & Tracking
```bash
# Get latest detections
GET /api/v1/cameras/{camera_id}/detections

# Get active object tracks
GET /api/v1/cameras/{camera_id}/tracks

# Get event history
GET /api/v1/cameras/{camera_id}/events?limit=50
```

### Detection Zones Management
```bash
# Add detection zone
POST /api/v1/cameras/{camera_id}/zones
{
  "name": "Front Door",
  "type": "rectangle",
  "coordinates": [100, 100, 400, 300],
  "restricted": true
}

# Get all zones for camera
GET /api/v1/cameras/{camera_id}/zones

# Remove detection zone
DELETE /api/v1/cameras/{camera_id}/zones/{zone_name}
```

### System Statistics
```bash
# Get Smart NVR statistics
GET /api/v1/cameras/nvr/statistics
```

## 📊 Smart NVR Dashboard Data

### Detection Response Format
```json
{
  "camera_id": 1,
  "detections": [
    {
      "object_type": "person",
      "confidence": 0.95,
      "bounding_box": [100, 50, 200, 300],
      "center": [200, 200],
      "area": 50000,
      "degirum_data": {
        "class_id": 0,
        "bbox_normalized": [0.1, 0.05, 0.3, 0.3],
        "score": 0.95
      }
    }
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Tracking Response Format
```json
{
  "camera_id": 1,
  "tracks": [
    {
      "track_id": "1_1705312200.123",
      "object_type": "person",
      "center": [200, 200],
      "confidence": 0.95,
      "age": 5,
      "hits": 10,
      "first_seen": "2024-01-15T10:29:50",
      "last_seen": "2024-01-15T10:30:00",
      "path": [[180, 190], [190, 195], [200, 200]]
    }
  ]
}
```

### Events Response Format
```json
{
  "camera_id": 1,
  "events": [
    {
      "type": "zone_violation",
      "object_type": "person",
      "confidence": 0.95,
      "zone_name": "Restricted Area",
      "timestamp": "2024-01-15T10:30:00",
      "location": [200, 200],
      "recorded_at": "2024-01-15T10:30:00"
    },
    {
      "type": "object_detected",
      "object_type": "person",
      "track_id": "1_1705312200.123",
      "timestamp": "2024-01-15T10:29:55",
      "location": [180, 190]
    }
  ],
  "total": 2
}
```

## 🎨 Visual Overlays

The Smart NVR system draws enhanced overlays on your camera feed:

### Detection Overlays
- **Green Boxes**: High confidence detections (>80%)
- **Yellow Boxes**: Medium confidence detections
- **Labels**: Object type and confidence score

### Tracking Overlays
- **Blue Circles**: Track centers
- **Track IDs**: Unique identifier for each tracked object
- **Blue Lines**: Movement paths (last 10 positions)

### Zone Overlays
- **Yellow Lines**: Regular detection zones
- **Red Lines**: Restricted zones
- **Zone Names**: Labels for each zone

## 🔧 Configuration & Customization

### Tracking Parameters
Edit `/backend/app/services/ai_detection_service.py`:

```python
# Tracking sensitivity
self.max_track_age = 30  # frames before track expires
self.min_track_hits = 3  # minimum detections to confirm track
self.track_distance_threshold = 100  # pixels for track matching

# Event parameters
self.record_buffer_seconds = 10  # seconds before/after event
self.max_events_per_camera = 100  # maximum stored events per camera
```

### Zone Types

#### Rectangle Zone
```python
zone_data = {
    "name": "Entrance",
    "type": "rectangle",
    "coordinates": [x1, y1, x2, y2],  # top-left, bottom-right
    "restricted": False
}
```

#### Polygon Zone
```python
zone_data = {
    "name": "Complex Area",
    "type": "polygon",
    "coordinates": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],  # polygon points
    "restricted": True
}
```

## 🚨 Event Types & Triggers

### 1. Object Detection Events
- **Trigger**: New object confirmed after minimum hits
- **Use Case**: Count people entering/leaving
- **Data**: Object type, location, track ID

### 2. Zone Violation Events
- **Trigger**: Object center enters restricted zone
- **Use Case**: Security perimeter monitoring
- **Data**: Zone name, object details, violation location

### 3. Loitering Detection Events
- **Trigger**: Object stays in view for 30+ seconds
- **Use Case**: Suspicious behavior detection
- **Data**: Duration, track details, location

## 💡 Usage Examples

### Frontend Integration (React)
```javascript
// Real-time event monitoring
const [events, setEvents] = useState([]);

useEffect(() => {
  const fetchEvents = async () => {
    const response = await fetch(`/api/v1/cameras/1/events?limit=10`);
    const data = await response.json();
    setEvents(data.events);
  };
  
  const interval = setInterval(fetchEvents, 5000); // Update every 5 seconds
  return () => clearInterval(interval);
}, []);

// Display active tracks
const [tracks, setTracks] = useState([]);

useEffect(() => {
  const fetchTracks = async () => {
    const response = await fetch(`/api/v1/cameras/1/tracks`);
    const data = await response.json();
    setTracks(data.tracks);
  };
  
  const interval = setInterval(fetchTracks, 1000); // Update every second
  return () => clearInterval(interval);
}, []);
```

### Adding Detection Zones
```javascript
// Add a restricted area zone
const addRestrictedZone = async () => {
  const zoneData = {
    name: "Private Office",
    type: "rectangle",
    coordinates: [100, 100, 400, 300],
    restricted: true
  };
  
  const response = await fetch(`/api/v1/cameras/1/zones`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(zoneData)
  });
  
  if (response.ok) {
    console.log('Zone added successfully');
  }
};
```

### Event Notifications
```javascript
// Monitor for security events
const checkSecurityEvents = async () => {
  const response = await fetch(`/api/v1/cameras/1/events?limit=5`);
  const data = await response.json();
  
  const securityEvents = data.events.filter(event => 
    event.type === 'zone_violation' || event.type === 'loitering_detected'
  );
  
  securityEvents.forEach(event => {
    // Send notification, trigger alarm, etc.
    console.log(`Security Alert: ${event.type} - ${event.object_type}`);
  });
};
```

## 🔍 Performance Optimization

### For Better Tracking
1. **Stable Camera**: Minimize camera shake for consistent tracking
2. **Good Lighting**: Ensure adequate lighting for reliable detection
3. **Optimal Frame Rate**: 10-15 FPS for good tracking performance
4. **Resolution**: 640x640 or 1080p for best accuracy vs performance

### For Event Accuracy
1. **Zone Placement**: Position zones away from camera edges
2. **Size Thresholds**: Adjust confidence thresholds based on environment
3. **Cooldown Tuning**: Adjust alert cooldowns based on your needs

## 🛠️ Troubleshooting

### Common Issues

1. **Tracks Not Persisting**
   - Check `track_distance_threshold` - may be too small
   - Ensure stable lighting conditions
   - Verify minimum hits threshold

2. **Too Many False Events**
   - Increase confidence threshold
   - Adjust zone boundaries
   - Increase alert cooldown period

3. **Missing Detections**
   - Lower confidence threshold
   - Check camera positioning
   - Verify DeGirum model performance

### Debug Information
```bash
# Check NVR statistics
curl http://localhost:8000/api/v1/cameras/nvr/statistics

# Monitor specific camera tracks
curl http://localhost:8000/api/v1/cameras/1/tracks

# View recent events
curl http://localhost:8000/api/v1/cameras/1/events?limit=20
```

Your Home-Vision-AI system is now a professional Smart NVR with advanced AI analytics, object tracking, and intelligent event detection!
