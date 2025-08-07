# Home Vision AI Mobile App

A React Native mobile application for the Home Vision AI system, providing remote monitoring and control of your smart home security cameras.

## Features

### 🔐 **Authentication**
- Simple login with username/password
- Secure token-based authentication
- Automatic session management
- Demo credentials included for testing

### 📹 **Camera Management**
- View all camera feeds in a grid layout
- Real-time camera status monitoring
- Start/stop camera streams
- Fullscreen camera view
- Camera health indicators

### 🔔 **Push Notifications**
- Real-time push notifications for events
- Firebase Cloud Messaging integration
- Configurable notification settings
- Swipe actions for notification management
- Unread notification badges

### 📊 **Dashboard**
- System overview with key statistics
- Quick access to main features
- Real-time status monitoring
- Recent events summary

### ⚙️ **Settings**
- User profile management
- Notification preferences
- App configuration options
- Camera and detection settings
- System information

## Prerequisites

- Node.js 18+ and npm
- React Native CLI
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)
- Firebase project with Cloud Messaging enabled

## Installation

### 1. Install Dependencies

```bash
cd mobile
npm install
```

### 2. iOS Setup (macOS only)

```bash
cd ios
pod install
cd ..
```

### 3. Firebase Configuration

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Cloud Messaging
3. Download `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
4. Place them in the appropriate directories:
   - Android: `android/app/google-services.json`
   - iOS: `ios/HomeVisionAI/GoogleService-Info.plist`

### 4. Environment Configuration

Create a `.env` file in the mobile directory:

```bash
# API Configuration
API_BASE_URL=http://localhost:8000/api/v1

# Firebase Configuration (optional - can be configured in Firebase console)
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

## Running the App

### Development Mode

```bash
# Start Metro bundler
npm start

# Run on Android
npm run android

# Run on iOS (macOS only)
npm run ios
```

### Production Build

```bash
# Android
cd android
./gradlew assembleRelease

# iOS (macOS only)
cd ios
xcodebuild -workspace HomeVisionAI.xcworkspace -scheme HomeVisionAI -configuration Release
```

## Project Structure

```
mobile/
├── src/
│   ├── components/          # Reusable UI components
│   │   └── CameraFeed.js   # Camera feed display component
│   ├── context/            # React Context providers
│   │   ├── AuthContext.js  # Authentication state management
│   │   └── NotificationContext.js # Notification state management
│   ├── screens/            # App screens
│   │   ├── LoginScreen.js  # Authentication screen
│   │   ├── HomeScreen.js   # Dashboard screen
│   │   ├── CameraScreen.js # Camera management screen
│   │   ├── NotificationsScreen.js # Notifications screen
│   │   └── SettingsScreen.js # Settings screen
│   ├── services/           # API and external services
│   │   ├── apiService.js   # Backend API client
│   │   └── notificationService.js # Push notification service
│   └── utils/              # Utility functions
├── App.js                  # Main app component
├── index.js                # App entry point
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

## API Integration

The mobile app communicates with the Home Vision AI backend through REST APIs:

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/verify` - Token verification

### Camera Endpoints
- `GET /cameras` - List all cameras
- `GET /cameras/{id}` - Get camera details
- `GET /cameras/{id}/frame` - Get camera frame
- `POST /cameras/{id}/start` - Start camera stream
- `POST /cameras/{id}/stop` - Stop camera stream

### Notification Endpoints
- `GET /notifications` - List notifications
- `PUT /notifications/{id}/read` - Mark as read
- `POST /notifications/subscribe` - Subscribe to topics

## Push Notifications

The app uses Firebase Cloud Messaging for push notifications:

### Supported Topics
- `general` - General system notifications
- `camera_events` - Camera detection events
- `system` - System alerts and updates

### Notification Types
- **Camera Events**: Motion detection, object detection
- **System Alerts**: Camera offline, storage issues
- **Security Alerts**: Unauthorized access attempts

## Development

### Adding New Screens

1. Create a new screen component in `src/screens/`
2. Add navigation route in `App.js`
3. Update tab navigator if needed

### Adding New API Endpoints

1. Add endpoint method in `src/services/apiService.js`
2. Create corresponding context or hook if needed
3. Update screens to use new functionality

### Styling

The app uses a consistent design system:
- Primary color: `#2196F3` (Blue)
- Success color: `#4CAF50` (Green)
- Warning color: `#FF9800` (Orange)
- Error color: `#F44336` (Red)

## Troubleshooting

### Common Issues

1. **Metro bundler issues**
   ```bash
   npm start -- --reset-cache
   ```

2. **iOS build issues**
   ```bash
   cd ios && pod install && cd ..
   ```

3. **Android build issues**
   ```bash
   cd android && ./gradlew clean && cd ..
   ```

4. **Firebase configuration issues**
   - Verify `google-services.json` is in the correct location
   - Check Firebase project settings
   - Ensure Cloud Messaging is enabled

### Debug Mode

Enable debug logging by setting environment variables:
```bash
export DEBUG=true
export API_DEBUG=true
```

## Contributing

1. Follow the existing code style and structure
2. Add proper error handling for API calls
3. Include loading states for async operations
4. Test on both Android and iOS devices
5. Update documentation for new features

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details. 