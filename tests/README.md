# Home-Vision-AI Test Suite

This directory contains comprehensive tests for the Home-Vision-AI system to verify that all components are working correctly.

## Test Components

### 🔍 **RTSP Camera Test** (`rtsp_test.py`)
Tests RTSP camera connectivity and displays video feeds.

**Features:**
- Test single camera connection
- Display live camera feeds
- Test multiple cameras simultaneously
- Interactive mode for manual testing

**Usage:**
```bash
# Test single camera
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --name "Front Door"

# Display camera feed
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --display --duration 30

# Test multiple cameras from config file
python tests/rtsp_test.py --config tests/camera_config.json

# Interactive mode
python tests/rtsp_test.py
```

### 🔥 **Firebase Test** (`firebase_test.py`)
Tests Firebase Cloud Messaging connectivity and notification sending.

**Features:**
- Test Firebase connection with credentials
- Send test notifications
- Test topic subscriptions
- Interactive notification testing

**Usage:**
```bash
# Run Firebase tests
python tests/firebase_test.py
```

### 🚀 **API Test** (`api_test.py`)
Tests FastAPI backend endpoints and functionality.

**Features:**
- Health check endpoint
- Camera management endpoints
- Event and notification endpoints
- Comprehensive API testing

**Usage:**
```bash
# Test all API endpoints
python tests/api_test.py --test all

# Test specific endpoint
python tests/api_test.py --test health
python tests/api_test.py --test cameras
python tests/api_test.py --test events
python tests/api_test.py --test notifications

# Test with custom URL
python tests/api_test.py --url http://localhost:8000
```

### 🧪 **Test Runner** (`run_tests.py`)
Orchestrates all tests and provides comprehensive system verification.

**Features:**
- Run all tests automatically
- Individual test selection
- Detailed test reporting
- System health summary

**Usage:**
```bash
# Run all tests
python tests/run_tests.py

# Run specific test
python tests/run_tests.py --test firebase
python tests/run_tests.py --test backend
python tests/run_tests.py --test rtsp
```

## Quick Start

### 1. Install Test Dependencies
```bash
pip install -r tests/requirements.txt
```

### 2. Run All Tests
```bash
python tests/run_tests.py
```

### 3. Test Individual Components
```bash
# Test RTSP cameras
python tests/rtsp_test.py --url "your_camera_rtsp_url"

# Test Firebase
python tests/firebase_test.py

# Test API (requires backend running)
python tests/api_test.py
```

## Test Configuration

### Camera Configuration (`camera_config.json`)
```json
{
  "Front Door": "rtsp://192.168.1.100:554/stream1",
  "Back Yard": "rtsp://192.168.1.101:554/stream1",
  "Garage": "rtsp://192.168.1.102:554/stream1"
}
```

### Environment Setup
Make sure you have:
- Firebase credentials file: `backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json`
- Backend running: `docker-compose up backend`
- Frontend running: `docker-compose up frontend`
- RTSP cameras accessible on your network

## Test Results

### ✅ **Passing Tests**
- All components working correctly
- System ready for production use

### ❌ **Failing Tests**
- Check error messages for specific issues
- Verify network connectivity
- Ensure services are running
- Check configuration files

## Troubleshooting

### RTSP Camera Issues
```bash
# Test with VLC first
vlc rtsp://your_camera_ip:554/stream1

# Check network connectivity
ping your_camera_ip
telnet your_camera_ip 554
```

### Firebase Issues
- Verify credentials file exists and is valid
- Check Firebase project configuration
- Ensure Cloud Messaging is enabled

### API Issues
- Ensure backend is running: `docker-compose up backend`
- Check API documentation: http://localhost:8000/docs
- Verify database connection

### Frontend Issues
- Install dependencies: `cd frontend && npm install`
- Start development server: `npm start`
- Check for build errors

## Test Output Examples

### Successful RTSP Test
```
Testing camera: Front Door
RTSP URL: rtsp://192.168.1.100:554/stream1
✅ Successfully connected to camera: Front Door
   Frame size: (1080, 1920, 3)
   FPS: 10.0
```

### Successful Firebase Test
```
Testing Firebase connection with credentials: backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json
✅ Firebase initialized successfully
   Project ID: home-vision-ai-xxxxx
```

### Successful API Test
```
Testing health endpoint...
✅ Health endpoint working
   Response: {'status': 'healthy'}

Testing cameras endpoint...
✅ Cameras endpoint working
   Found 2 cameras
   - Front Door Camera: online
   - Back Yard Camera: online
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -r tests/requirements.txt
    python tests/run_tests.py --test all
```

## Contributing

When adding new features:
1. Add corresponding tests
2. Update test documentation
3. Ensure all tests pass
4. Add test cases for edge cases

## Support

For test-related issues:
1. Check the test output for specific error messages
2. Verify system requirements are met
3. Test individual components
4. Check network and service connectivity 