# Home-Vision-AI Project Structure

## Backend (FastAPI)
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── camera.py           # Camera model
│   │   ├── event.py            # Event detection model
│   │   ├── notification.py     # Notification model
│   │   └── user.py             # User model
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cameras.py  # Camera management endpoints
│   │   │   │   ├── events.py   # Event detection endpoints
│   │   │   │   ├── notifications.py # Notification endpoints
│   │   │   │   └── auth.py     # Authentication endpoints
│   │   │   └── api.py          # API router
│   │   └── deps.py             # Dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT authentication
│   │   ├── config.py           # Environment configuration
│   │   └── database.py         # Database connection
│   ├── services/
│   │   ├── __init__.py
│   │   ├── camera_service.py   # Camera stream management
│   │   ├── detection_service.py # AI detection logic
│   │   ├── notification_service.py # Firebase notification service
│   │   └── video_service.py    # Video processing and storage
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── video_utils.py      # Video processing utilities
│   │   └── ai_utils.py         # AI model utilities
│   └── tests/
│       ├── __init__.py
│       ├── test_api.py
│       └── test_services.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Frontend (React)
```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── ErrorBoundary.jsx
│   │   ├── camera/
│   │   │   ├── CameraGrid.jsx
│   │   │   ├── CameraFeed.jsx
│   │   │   ├── CameraSettings.jsx
│   │   │   └── CameraStatus.jsx
│   │   ├── events/
│   │   │   ├── EventList.jsx
│   │   │   ├── EventDetail.jsx
│   │   │   ├── EventVideo.jsx
│   │   │   └── EventFilters.jsx
│   │   ├── notifications/
│   │   │   ├── NotificationCenter.jsx
│   │   │   ├── NotificationSettings.jsx
│   │   │   └── NotificationItem.jsx
│   │   └── dashboard/
│   │       ├── Dashboard.jsx
│   │       ├── Stats.jsx
│   │       └── Charts.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Cameras.jsx
│   │   ├── Events.jsx
│   │   ├── Notifications.jsx
│   │   └── Settings.jsx
│   ├── services/
│   │   ├── api.js              # API client
│   │   ├── auth.js             # Authentication service
│   │   ├── notifications.js    # Firebase notification service
│   │   └── websocket.js        # WebSocket for real-time updates
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useCameras.js
│   │   ├── useEvents.js
│   │   └── useNotifications.js
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   ├── CameraContext.jsx
│   │   └── NotificationContext.jsx
│   ├── utils/
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── validators.js
│   ├── styles/
│   │   ├── index.css
│   │   ├── components.css
│   │   └── variables.css
│   ├── App.jsx
│   ├── index.js
│   └── routes.jsx
├── package.json
├── tailwind.config.js
└── vite.config.js
```

## Mobile App (React Native)
```
mobile/
├── src/
│   ├── components/
│   │   ├── CameraFeed.js
│   │   ├── EventList.js
│   │   ├── NotificationItem.js
│   │   └── common/
│   ├── screens/
│   │   ├── HomeScreen.js
│   │   ├── CameraScreen.js
│   │   ├── EventsScreen.js
│   │   ├── NotificationsScreen.js
│   │   └── SettingsScreen.js
│   ├── services/
│   │   ├── api.js
│   │   ├── notifications.js
│   │   └── storage.js
│   ├── navigation/
│   │   └── AppNavigator.js
│   ├── utils/
│   │   └── helpers.js
│   └── App.js
├── package.json
├── app.json
└── metro.config.js
```

## Shared Configuration
```
config/
├── firebase.json               # Firebase configuration
├── .env.example               # Environment variables template
└── docker-compose.yml         # Full stack orchestration
```

## Documentation
```
docs/
├── api.md                     # API documentation
├── setup.md                   # Setup instructions
├── deployment.md              # Deployment guide
└── architecture.md            # System architecture
``` 