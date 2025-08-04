# Notification Testing Guide

This guide covers how to test notifications in the Home-Vision-AI system, including Firebase Cloud Messaging setup and various notification types.

## Prerequisites

### 1. Firebase Setup
Ensure you have:
- Firebase project created
- Service account credentials file
- Cloud Messaging enabled
- Proper permissions configured

### 2. Credentials File
The Firebase credentials file should be located at:
```
backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json
```

## Testing Methods

### 1. Firebase Test Script (Recommended)

The enhanced Firebase test script provides comprehensive notification testing:

```bash
# Basic connection test
python tests/firebase_test.py --test connection

# Send basic notification
python tests/firebase_test.py --test basic --topic "test_topic" --title "Test" --body "Hello World"

# Test detection notification
python tests/firebase_test.py --test detection --camera "Front Door Camera"

# Test camera status notification
python tests/firebase_test.py --test status --camera "Back Yard Camera" --status "offline"

# Test system notification
python tests/firebase_test.py --test system --title "System Alert" --body "Maintenance scheduled"

# Run comprehensive tests
python tests/firebase_test.py --test comprehensive
```

### 2. Interactive Mode

For interactive testing with menu options:

```bash
python tests/firebase_test.py
```

This provides options for:
- Basic test notifications
- Detection event notifications
- Camera status notifications
- System notifications
- Topic subscription/unsubscription
- Comprehensive test suite

### 3. API Testing

Test notification endpoints via the API:

```bash
# Test notifications endpoint
python tests/api_test.py --test notifications

# Test all endpoints including notifications
python tests/api_test.py --test all
```

## Notification Types

### 1. Detection Event Notifications

These are sent when AI detects objects (cats, humans, etc.):

```bash
python tests/firebase_test.py --test detection --camera "Front Door Camera"
```

**Payload includes:**
- Event ID
- Camera ID and name
- Object type (cat, human, etc.)
- Confidence score
- Timestamp

### 2. Camera Status Notifications

These are sent when camera status changes:

```bash
python tests/firebase_test.py --test status --camera "Back Yard Camera" --status "offline"
```

**Payload includes:**
- Camera name
- Status (online/offline/error)
- Timestamp
- Error message (if applicable)

### 3. System Notifications

These are for system-wide alerts:

```bash
python tests/firebase_test.py --test system --title "System Alert" --body "AI model updated"
```

**Payload includes:**
- Notification type
- Priority level
- Timestamp
- Source identifier

## Topic Management

### Available Topics

- `test_topic`: General testing
- `detection_events`: AI detection alerts
- `camera_status`: Camera status changes
- `system_notifications`: System-wide alerts

### Subscribe Devices to Topics

```bash
# Interactive topic subscription
python tests/firebase_test.py
# Choose option 5: Subscribe devices to topic
```

### Unsubscribe Devices from Topics

```bash
# Interactive topic unsubscription
python tests/firebase_test.py
# Choose option 6: Unsubscribe devices from topic
```

## Mobile App Testing

### 1. Get Device Token

From your mobile app, get the FCM device token and use it for testing:

```bash
python tests/firebase_test.py
# Choose option 5 and enter your device token
```

### 2. Test Direct Notifications

Send notifications directly to your device:

```bash
python tests/firebase_test.py --test basic --topic "your_device_topic"
```

## Troubleshooting

### Common Issues

1. **Credentials File Not Found**
   ```
   ❌ Credentials file not found: backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json
   ```
   **Solution**: Ensure the Firebase credentials file exists and is accessible.

2. **Firebase Initialization Failed**
   ```
   ❌ Failed to initialize Firebase: [Errno 2] No such file or directory
   ```
   **Solution**: Check credentials file path and permissions.

3. **Notification Send Failed**
   ```
   ❌ Failed to send notification: Invalid (registration) token provided
   ```
   **Solution**: Verify topic exists or device token is valid.

4. **Topic Subscription Failed**
   ```
   ❌ Failed to subscribe to topic: Invalid (registration) token provided
   ```
   **Solution**: Ensure device tokens are valid and not expired.

### Debug Steps

1. **Check Firebase Connection**
   ```bash
   python tests/firebase_test.py --test connection
   ```

2. **Verify Credentials**
   ```bash
   # Check if credentials file exists
   ls -la backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json
   
   # Check file permissions
   file backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json
   ```

3. **Test Basic Notification**
   ```bash
   python tests/firebase_test.py --test basic
   ```

4. **Check Firebase Console**
   - Verify project settings
   - Check Cloud Messaging is enabled
   - Review service account permissions

## Integration Testing

### 1. End-to-End Testing

Test the complete notification flow:

```bash
# 1. Test camera connectivity
python tests/rtsp_test.py --url "rtsp://your_camera_ip:554/stream1"

# 2. Test notification system
python tests/firebase_test.py --test comprehensive

# 3. Test API endpoints
python tests/api_test.py --test all
```

### 2. Real-Time Testing

For real-time notification testing:

1. Start the backend server
2. Configure cameras
3. Enable AI detection
4. Monitor notifications in real-time

```bash
# Start backend
docker-compose up backend

# In another terminal, monitor logs
docker-compose logs -f backend
```

## Performance Testing

### 1. Load Testing

Test notification system under load:

```bash
# Send multiple notifications rapidly
for i in {1..10}; do
  python tests/firebase_test.py --test basic --title "Test $i" --body "Load test notification $i"
  sleep 1
done
```

### 2. Concurrent Testing

Test multiple notification types simultaneously:

```bash
# Run comprehensive tests
python tests/firebase_test.py --test comprehensive
```

## Best Practices

### 1. Testing Strategy

- Test each notification type individually
- Verify payload structure
- Check mobile app reception
- Monitor Firebase console for delivery status

### 2. Error Handling

- Always check for connection errors
- Verify credentials before testing
- Handle failed notifications gracefully
- Log all test results

### 3. Security

- Keep credentials file secure
- Use test topics for development
- Monitor notification usage
- Implement rate limiting if needed

## Monitoring and Logs

### 1. Firebase Console

Monitor notifications in Firebase Console:
- Go to Firebase Console > Cloud Messaging
- Check delivery statistics
- Review error reports

### 2. Application Logs

Monitor application logs for notification events:

```bash
# Backend logs
docker-compose logs backend | grep notification

# Test script logs
python tests/firebase_test.py --test comprehensive 2>&1 | tee notification_test.log
```

### 3. Mobile App Logs

Check mobile app logs for notification reception and handling.

## Next Steps

After successful notification testing:

1. **Configure Production Topics**: Set up proper topic structure
2. **Implement Error Handling**: Add robust error handling
3. **Set Up Monitoring**: Configure alerts for notification failures
4. **Document Procedures**: Create runbooks for notification management
5. **Performance Optimization**: Optimize notification delivery

## Support

For notification testing issues:

1. Check this guide for common solutions
2. Review Firebase documentation
3. Check application logs for errors
4. Verify network connectivity
5. Test with minimal configuration first 