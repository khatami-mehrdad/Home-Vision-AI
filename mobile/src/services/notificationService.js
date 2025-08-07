import messaging from '@react-native-firebase/messaging';
import PushNotification from 'react-native-push-notification';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiService } from './apiService';

class NotificationService {
  constructor() {
    this.fcmToken = null;
    this.isInitialized = false;
  }

  async initialize() {
    if (this.isInitialized) return;

    try {
      // Request permission
      const authStatus = await messaging().requestPermission();
      const enabled =
        authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
        authStatus === messaging.AuthorizationStatus.PROVISIONAL;

      if (enabled) {
        console.log('Authorization status:', authStatus);
        
        // Get FCM token
        this.fcmToken = await messaging().getToken();
        console.log('FCM Token:', this.fcmToken);
        
        // Store token
        await AsyncStorage.setItem('fcmToken', this.fcmToken);
        
        // Subscribe to topics
        await this.subscribeToTopics();
        
        // Set up message handlers
        this.setupMessageHandlers();
        
        // Configure local notifications
        this.configureLocalNotifications();
        
        this.isInitialized = true;
      }
    } catch (error) {
      console.error('Failed to initialize notifications:', error);
    }
  }

  async subscribeToTopics() {
    try {
      if (!this.fcmToken) return;

      // Subscribe to general notifications
      await messaging().subscribeToTopic('general');
      
      // Subscribe to camera events
      await messaging().subscribeToTopic('camera_events');
      
      // Subscribe to system notifications
      await messaging().subscribeToTopic('system');
      
      // Register token with backend
      await apiService.subscribeToNotifications(this.fcmToken, [
        'general',
        'camera_events',
        'system'
      ]);
      
      console.log('Subscribed to notification topics');
    } catch (error) {
      console.error('Failed to subscribe to topics:', error);
    }
  }

  setupMessageHandlers() {
    // Handle background messages
    messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('Message handled in the background!', remoteMessage);
      
      // Show local notification
      this.showLocalNotification({
        title: remoteMessage.notification?.title || 'Home Vision',
        message: remoteMessage.notification?.body || 'New notification',
        data: remoteMessage.data,
      });
    });

    // Handle foreground messages
    const unsubscribe = messaging().onMessage(async remoteMessage => {
      console.log('A new FCM message arrived!', remoteMessage);
      
      // Show local notification
      this.showLocalNotification({
        title: remoteMessage.notification?.title || 'Home Vision',
        message: remoteMessage.notification?.body || 'New notification',
        data: remoteMessage.data,
      });
    });

    return unsubscribe;
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
        // You can navigate to specific screens based on notification data
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

  async getToken() {
    try {
      const token = await messaging().getToken();
      return token;
    } catch (error) {
      console.error('Failed to get FCM token:', error);
      return null;
    }
  }

  async unsubscribeFromTopics() {
    try {
      if (!this.fcmToken) return;

      await messaging().unsubscribeFromTopic('general');
      await messaging().unsubscribeFromTopic('camera_events');
      await messaging().unsubscribeFromTopic('system');
      
      await apiService.unsubscribeFromNotifications(this.fcmToken, [
        'general',
        'camera_events',
        'system'
      ]);
      
      console.log('Unsubscribed from notification topics');
    } catch (error) {
      console.error('Failed to unsubscribe from topics:', error);
    }
  }
}

export const notificationService = new NotificationService();

export const initializeNotifications = () => {
  notificationService.initialize();
}; 