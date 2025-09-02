import PushNotification from 'react-native-push-notification';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiService } from './apiService';

class NotificationService {
  constructor() {
    this.isInitialized = false;
  }

  async initialize() {
    if (this.isInitialized) return;

    try {
      // Configure local notifications
      this.configureLocalNotifications();
      
      this.isInitialized = true;
      console.log('Notification service initialized');
    } catch (error) {
      console.error('Failed to initialize notifications:', error);
    }
  }

  configureLocalNotifications() {
    PushNotification.configure({
      // (optional) Called when Token is generated (iOS and Android)
      onRegister: function (token) {
        console.log("TOKEN:", token);
      },

      // (required) Called when a remote is received or opened, or local notification is opened
      onNotification: function (notification) {
        console.log("NOTIFICATION:", notification);
        
        // Process the notification
        if (notification.data) {
          this.handleNotificationData(notification.data);
        }
      },

      // (optional) Called when the user fails to register for remote notifications. Typically occurs when APNS is having issues, or the device is a simulator. (iOS)
      onRegistrationError: function(err) {
        console.error(err.message, err);
      },

      // IOS ONLY (optional): default: all - Permissions to register.
      permissions: {
        alert: true,
        badge: true,
        sound: true,
      },

      // Should the initial notification be popped automatically
      // default: true
      popInitialNotification: true,

      /**
       * (optional) default: true
       * - false: it will not be called if the app was closed by the user or killed by the system.
       * - true: it will be called even if the app was closed by the user or killed by the system.
       */
      requestPermissions: true,
    });

    // Create notification channel for Android
    PushNotification.createChannel(
      {
        channelId: "home-vision-channel",
        channelName: "Home Vision Notifications",
        channelDescription: "Notifications from Home Vision AI",
        playSound: true,
        soundName: "default",
        importance: 4,
        vibrate: true,
      },
      (created) => console.log(`createChannel returned '${created}'`)
    );
  }

  showLocalNotification({ title, message, data = {} }) {
    PushNotification.localNotification({
      channelId: "home-vision-channel",
      title: title,
      message: message,
      data: data,
      playSound: true,
      soundName: "default",
      importance: "high",
      priority: "high",
      vibrate: true,
      vibration: 300,
      autoCancel: true,
      largeIcon: "ic_launcher",
      smallIcon: "ic_notification",
      bigText: message,
      subText: "Home Vision AI",
      color: "#2196F3",
      number: 10,
    });
  }

  handleNotificationData(data) {
    // Handle different types of notifications
    switch (data.type) {
      case 'camera_event':
        // Navigate to camera screen or show camera feed
        console.log('Camera event detected:', data);
        break;
      case 'motion_detected':
        // Show motion detection alert
        console.log('Motion detected:', data);
        break;
      case 'system_alert':
        // Show system alert
        console.log('System alert:', data);
        break;
      default:
        console.log('Unknown notification type:', data);
    }
  }

  // Simulate push notification for testing
  simulateNotification(type, title, message) {
    this.showLocalNotification({
      title: title,
      message: message,
      data: { type: type }
    });
  }

  async subscribeToTopics() {
    try {
      console.log('Subscribed to notification topics (simulated)');
    } catch (error) {
      console.error('Failed to subscribe to topics:', error);
    }
  }

  async unsubscribeFromTopics() {
    try {
      console.log('Unsubscribed from notification topics (simulated)');
    } catch (error) {
      console.error('Failed to unsubscribe from topics:', error);
    }
  }
}

export const notificationService = new NotificationService();

export const initializeNotifications = () => {
  notificationService.initialize();
}; 