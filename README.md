
# Home-Vision-AI 🛡️📹  
*Edge-based AI Camera System for Home Security, Cat Detection, and Smart Automation*

## Overview

Home-Vision-AI is a comprehensive smart home vision system powered by real-time object detection on edge devices. Built with FastAPI backend, React frontend, and Firebase notifications, it provides a complete solution for home security monitoring with AI-powered detection capabilities.

## Features

### 🎥 **Multi-Camera Support**
- Real-time RTSP stream processing
- Support for multiple camera brands (Hikvision, Dahua, Axis, Foscam)
- Live video feeds with frame-by-frame analysis
- Camera health monitoring and status tracking

### 🤖 **AI-Powered Detection**
- Cat detection (primary focus)
- Human detection capabilities
- Configurable confidence thresholds
- Real-time object tracking and bounding boxes

### 📱 **Web & Mobile Interface**
- Modern React web application
- Real-time camera grid view
- Event timeline and video playback
- Responsive design for mobile devices
- Push notifications via Firebase

### 🔔 **Smart Notifications**
- Firebase Cloud Messaging integration
- Instant push notifications on detection events
- Configurable notification rules
- Browser and mobile app notifications

### 📊 **Event Management**
- Automatic video recording on detection
- Event timeline with thumbnails
- Video playback and download
- Event filtering and search

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │  Firebase Cloud │
│                 │    │                 │    │   Messaging     │
│ • Camera Grid   │◄──►│ • RTSP Streams  │◄──►│ • Push Notifications│
│ • Event Viewer  │    │ • AI Detection  │    │ • Topic Management│
│ • Real-time UI  │    │ • Video Storage │    │ • Device Tokens  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   RTSP Cameras  │
│                 │    │                 │    │                 │
│ • Event Storage │    │ • Session Cache │    │ • Live Streams  │
│ • User Data     │    │ • Real-time Data│    │ • IP Cameras    │
│ • Configuration │    │ • Pub/Sub       │    │ • Edge Devices  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + Python | REST API, RTSP processing, AI inference |
| **Frontend** | React + TypeScript | Web interface, real-time updates |
| **Database** | PostgreSQL | Event storage, user data |
| **Cache** | Redis | Session management, real-time data |
| **Notifications** | Firebase Cloud Messaging | Push notifications |
| **AI/ML** | DeGirum PySDK / OpenCV | Object detection |
| **Video** | OpenCV + GStreamer | Stream processing |
| **Deployment** | Docker + Docker Compose | Containerized deployment |

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Firebase project with Cloud Messaging
- RTSP-enabled cameras

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Home-Vision-AI

# Create environment file
cp .env.example .env
# Edit .env with your Firebase configuration
```

### 2. Firebase Setup
1. Create Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Cloud Messaging
3. Generate service account key → `firebase-credentials.json`
4. Get VAPID key from Project Settings

### 3. Start Application
```bash
# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 4. Add Cameras
1. Access web interface at http://localhost:3000
2. Navigate to Cameras section
3. Add your RTSP camera streams
4. Configure detection settings

## API Documentation

### Camera Endpoints
- `GET /api/v1/cameras` - List all cameras
- `POST /api/v1/cameras` - Add new camera
- `GET /api/v1/cameras/{id}/frame` - Get live frame
- `POST /api/v1/cameras/{id}/start` - Start streaming
- `POST /api/v1/cameras/{id}/stop` - Stop streaming

### Event Endpoints
- `GET /api/v1/events` - List detection events
- `GET /api/v1/events/{id}` - Get event details
- `DELETE /api/v1/events/{id}` - Delete event

### Notification Endpoints
- `GET /api/v1/notifications` - List notifications
- `POST /api/v1/notifications/subscribe` - Subscribe to topics
- `PUT /api/v1/notifications/{id}/read` - Mark as read

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

## Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/homevision
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=11520

# Firebase
FIREBASE_CREDENTIALS_FILE=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id

# AI Detection
DETECTION_CONFIDENCE_THRESHOLD=0.7
DETECTION_MODEL_PATH=/path/to/model

# Camera Settings
CAMERA_FRAME_RATE=10
CAMERA_RESOLUTION=1080p
```

#### Frontend (.env.local)
```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_VAPID_KEY=your_vapid_key
```

## Camera Setup

### Supported Camera Types
- **RTSP Cameras**: Hikvision, Dahua, Axis, Foscam
- **IP Cameras**: Any camera with RTSP support
- **USB Cameras**: Direct USB connection

### RTSP URL Format
```
rtsp://username:password@camera_ip:554/stream1
rtsp://camera_ip:554/stream1
rtsp://camera_ip:554/h264Preview_01_main
```

### Camera Configuration
1. **Network Setup**: Ensure cameras are on same network
2. **RTSP Testing**: Test with VLC player first
3. **Authentication**: Configure username/password if required
4. **Port Forwarding**: For remote access (optional)

## AI Detection

### Supported Models
- **DeGirum PySDK**: Optimized for edge devices
- **OpenCV DNN**: Pre-trained models
- **Custom Models**: TensorFlow/PyTorch models

### Detection Classes
- **Cat Detection**: Primary focus
- **Human Detection**: Security monitoring
- **Object Detection**: General purpose
- **Custom Classes**: Configurable

### Performance Optimization
- **Hardware Acceleration**: GPU/TPU support
- **Model Quantization**: Reduced precision for speed
- **Batch Processing**: Multiple frame analysis
- **Edge Computing**: Local processing

## Security Features

### Authentication
- JWT-based authentication
- Role-based access control
- Session management with Redis

### Network Security
- HTTPS/TLS encryption
- Firewall configuration
- VPN support for remote access

### Data Protection
- Encrypted video storage
- Secure API endpoints
- Audit logging

## Monitoring & Maintenance

### Health Checks
- Application health endpoints
- Database connectivity checks
- Camera stream monitoring

### Logging
- Structured logging with JSON
- Error tracking and alerting
- Performance metrics

### Backup Strategy
- Database backups
- Video file retention
- Configuration backups

## Deployment

### Production Deployment
1. **SSL/TLS**: Configure certificates
2. **Load Balancing**: Nginx reverse proxy
3. **Monitoring**: Prometheus + Grafana
4. **Backup**: Automated backup scripts

### Docker Deployment
```bash
# Production build
docker-compose -f docker-compose.prod.yml up -d

# With custom configuration
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### Cloud Deployment
- **AWS**: ECS/EKS with RDS
- **Google Cloud**: GKE with Cloud SQL
- **Azure**: AKS with Azure Database

## Troubleshooting

### Common Issues

#### Camera Stream Issues
```bash
# Test RTSP stream
vlc rtsp://camera_ip:554/stream1

# Check network connectivity
ping camera_ip
telnet camera_ip 554
```

#### Firebase Issues
- Verify service account credentials
- Check VAPID key configuration
- Ensure Cloud Messaging is enabled

#### Performance Issues
- Monitor CPU/memory usage
- Check database query performance
- Optimize video processing pipeline

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# View real-time logs
docker-compose logs -f backend
```

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests for new features
5. Submit pull request

### Code Standards
- **Python**: Black, isort, flake8
- **JavaScript**: ESLint, Prettier
- **TypeScript**: Strict mode enabled

### Testing
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# Integration tests
docker-compose -f docker-compose.test.yml up
```

## Roadmap

### Phase 1: Core Features ✅
- [x] Multi-camera RTSP support
- [x] AI detection (cat/human)
- [x] Web interface
- [x] Firebase notifications
- [x] Event recording

### Phase 2: Advanced Features 🚧
- [ ] Mobile app (React Native)
- [ ] Advanced AI models
- [ ] Cloud storage integration
- [ ] Multi-user support
- [ ] Advanced analytics

### Phase 3: Automation 🌐
- [ ] Home Assistant integration
- [ ] IFTTT/Zapier support
- [ ] Custom automation rules
- [ ] Voice assistant integration
- [ ] Smart home device control

## Support

- **Documentation**: [Setup Guide](SETUP.md)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Wiki**: Project Wiki

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **DeGirum**: AI acceleration technology
- **OpenCV**: Computer vision library
- **FastAPI**: Modern web framework
- **React**: Frontend framework
- **Firebase**: Cloud services

---

**Home-Vision-AI** - Making home security intelligent and accessible 🏠🔒

