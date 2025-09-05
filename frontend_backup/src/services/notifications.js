import { initializeApp } from 'firebase/app';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';

// Firebase configuration
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

class NotificationService {
  constructor() {
    this.isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
    this.permission = 'default';
    this.token = null;
    this.onMessageCallback = null;
  }

  async initialize() {
    if (!this.isSupported) {
      console.warn('Push notifications are not supported');
      return false;
    }

    try {
      // Request permission
      const permission = await Notification.requestPermission();
      this.permission = permission;

      if (permission !== 'granted') {
        console.warn('Notification permission denied');
        return false;
      }

      // Get FCM token
      this.token = await this.getFCMToken();
      
      // Set up message listener
      this.setupMessageListener();

      return true;
    } catch (error) {
      console.error('Failed to initialize notifications:', error);
      return false;
    }
  }

  async getFCMToken() {
    try {
      const token = await getToken(messaging, {
        vapidKey: process.env.REACT_APP_FIREBASE_VAPID_KEY,
      });

      if (token) {
        console.log('FCM Token:', token);
        return token;
      } else {
        console.warn('No registration token available');
        return null;
      }
    } catch (error) {
      console.error('Failed to get FCM token:', error);
      return null;
    }
  }

  setupMessageListener() {
    onMessage(messaging, (payload) => {
      console.log('Message received:', payload);
      
      // Show browser notification
      this.showBrowserNotification(payload);
      
      // Call callback if set
      if (this.onMessageCallback) {
        this.onMessageCallback(payload);
      }
    });
  }

  showBrowserNotification(payload) {
    const { notification, data } = payload;
    
    if (Notification.permission === 'granted') {
      const browserNotification = new Notification(notification.title, {
        body: notification.body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        data: data,
        requireInteraction: true,
        actions: [
          {
            action: 'view',
            title: 'View',
          },
          {
            action: 'dismiss',
            title: 'Dismiss',
          },
        ],
      });

      browserNotification.onclick = (event) => {
        event.preventDefault();
        browserNotification.close();
        
        // Handle notification click
        if (data?.event_id) {
          window.location.href = `/events/${data.event_id}`;
        } else if (data?.camera_id) {
          window.location.href = `/cameras/${data.camera_id}`;
        }
      };

      browserNotification.onaction = (event) => {
        if (event.action === 'view') {
          browserNotification.close();
          if (data?.event_id) {
            window.location.href = `/events/${data.event_id}`;
          }
        } else if (event.action === 'dismiss') {
          browserNotification.close();
        }
      };
    }
  }

  onMessage(callback) {
    this.onMessageCallback = callback;
  }

  async subscribeToTopic(topic) {
    if (!this.token) {
      console.warn('No FCM token available');
      return false;
    }

    try {
      const response = await fetch('/api/v1/notifications/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: this.token,
          topic: topic,
        }),
      });

      if (response.ok) {
        console.log(`Subscribed to topic: ${topic}`);
        return true;
      } else {
        console.error('Failed to subscribe to topic');
        return false;
      }
    } catch (error) {
      console.error('Error subscribing to topic:', error);
      return false;
    }
  }

  async unsubscribeFromTopic(topic) {
    if (!this.token) {
      console.warn('No FCM token available');
      return false;
    }

    try {
      const response = await fetch('/api/v1/notifications/unsubscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: this.token,
          topic: topic,
        }),
      });

      if (response.ok) {
        console.log(`Unsubscribed from topic: ${topic}`);
        return true;
      } else {
        console.error('Failed to unsubscribe from topic');
        return false;
      }
    } catch (error) {
      console.error('Error unsubscribing from topic:', error);
      return false;
    }
  }

  getToken() {
    return this.token;
  }

  getPermission() {
    return this.permission;
  }

  isSupported() {
    return this.isSupported;
  }
}

// Create singleton instance
const notificationService = new NotificationService();

export default notificationService; 