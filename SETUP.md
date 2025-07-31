# Home-Vision-AI Setup Guide

This guide will help you set up the complete Home-Vision-AI system with FastAPI backend, React frontend, and Firebase notifications.

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Firebase project with Cloud Messaging enabled

## Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Home-Vision-AI
```

### 2. Environment Configuration

Create a `.env` file in the root directory:
```bash
# Firebase Configuration
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id
REACT_APP_FIREBASE_VAPID_KEY=your_vapid_key

# Backend Configuration
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=postgresql://homevision:homevision123@postgres:5432/homevision
REDIS_URL=redis://redis:6379
```

### 3. Firebase Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Cloud Messaging
3. Generate a service account key and save as `firebase-credentials.json` in the root directory
4. Get your VAPID key from Project Settings > Cloud Messaging

### 4. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Local Development Setup

### Backend Development

1. Create a Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
# Edit .env.local with your Firebase configuration
```

3. Start the development server:
```bash
npm start
```

## Camera Configuration

### Adding Cameras

1. **RTSP Cameras**: Configure your cameras to stream via RTSP
   - Example RTSP URL: `rtsp://username:password@192.168.1.100:554/stream1`

2. **IP Cameras**: Ensure cameras are accessible on your local network
   - Common brands: Hikvision, Dahua, Axis, Foscam

3. **Test Camera Streams**:
   ```bash
   # Test with VLC
   vlc rtsp://your_camera_ip:554/stream1
   ```

### Camera Setup Steps

1. Access the web interface at http://localhost:3000
2. Navigate to Cameras section
3. Click "Add Camera"
4. Enter camera details:
   - Name: "Front Door Camera"
   - RTSP URL: Your camera's RTSP stream URL
   - Location: "Front Door"
   - Frame Rate: 10 (recommended)
   - Resolution: 1080p

## AI Detection Setup

### Model Configuration

1. **DeGirum PySDK** (Recommended for edge devices):
   ```bash
   # Install DeGirum PySDK
   pip install degirum
   
   # Download cat detection model
   # Follow DeGirum documentation for model setup
   ```

2. **OpenCV DNN** (Alternative):
   ```bash
   # Download pre-trained models
   wget https://github.com/opencv/opencv/raw/master/samples/dnn/face_detector/opencv_face_detector_uint8.pb
   ```

### Detection Configuration

Update `backend/app/core/config.py`:
```python
DETECTION_MODEL_PATH = "/path/to/your/model"
DETECTION_CONFIDENCE_THRESHOLD = 0.7
```

## Notification Setup

### Firebase Configuration

1. **Enable Cloud Messaging**:
   - Go to Firebase Console > Project Settings
   - Enable Cloud Messaging
   - Generate VAPID key

2. **Service Account**:
   - Go to Project Settings > Service Accounts
   - Generate new private key
   - Save as `firebase-credentials.json`

3. **Web App Configuration**:
   - Add web app to Firebase project
   - Copy configuration to frontend `.env.local`

### Notification Topics

The system uses these Firebase topics:
- `detection_events`: For object detection alerts
- `camera_status`: For camera status changes
- `system_notifications`: For system-wide notifications

## Database Setup

### PostgreSQL

The application uses PostgreSQL for data storage. With Docker Compose, the database is automatically created.

For manual setup:
```sql
CREATE DATABASE homevision;
CREATE USER homevision WITH PASSWORD 'homevision123';
GRANT ALL PRIVILEGES ON DATABASE homevision TO homevision;
```

### Database Migrations

Run migrations to create tables:
```bash
cd backend
alembic upgrade head
```

## Security Considerations

### Production Deployment

1. **Change Default Passwords**:
   - Update database passwords
   - Change SECRET_KEY
   - Use strong passwords for all services

2. **SSL/TLS**:
   - Configure SSL certificates
   - Use HTTPS for all communications

3. **Network Security**:
   - Place cameras on isolated network
   - Use VPN for remote access
   - Configure firewall rules

4. **Environment Variables**:
   - Never commit sensitive data
   - Use secure secret management

## Troubleshooting

### Common Issues

1. **Camera Stream Not Working**:
   - Check RTSP URL format
   - Verify network connectivity
   - Test with VLC player

2. **Firebase Notifications Not Working**:
   - Verify Firebase configuration
   - Check browser notification permissions
   - Ensure VAPID key is correct

3. **AI Detection Not Working**:
   - Verify model path
   - Check model compatibility
   - Review detection confidence threshold

4. **Database Connection Issues**:
   - Check PostgreSQL service
   - Verify connection string
   - Check network connectivity

### Logs

View application logs:
```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# All logs
docker-compose logs -f
```

## Performance Optimization

### Backend Optimization

1. **Database Indexing**:
   - Add indexes for frequently queried fields
   - Optimize query performance

2. **Caching**:
   - Use Redis for session storage
   - Cache frequently accessed data

3. **Video Processing**:
   - Optimize frame processing
   - Use hardware acceleration when available

### Frontend Optimization

1. **Image Optimization**:
   - Compress camera frames
   - Use appropriate image formats

2. **Real-time Updates**:
   - Implement WebSocket connections
   - Use efficient polling strategies

## Monitoring and Maintenance

### Health Checks

The application includes health check endpoints:
- Backend: `GET /health`
- Frontend: Built-in React health checks

### Backup Strategy

1. **Database Backups**:
   ```bash
   docker-compose exec postgres pg_dump -U homevision homevision > backup.sql
   ```

2. **Video Storage**:
   - Regular backups of video files
   - Implement retention policies

3. **Configuration Backups**:
   - Backup environment files
   - Version control configuration

## Support and Contributing

For issues and contributions:
1. Check existing issues
2. Create detailed bug reports
3. Follow contribution guidelines
4. Test thoroughly before submitting

## License

This project is licensed under the Apache License 2.0. 