#!/usr/bin/env python3
"""
Firebase Test Script
Tests Firebase Cloud Messaging connectivity and notification sending
Enhanced with comprehensive notification testing capabilities
"""

import firebase_admin
from firebase_admin import credentials, messaging
import json
import sys
import os
import time
import argparse
from typing import List, Dict, Any

# Global Firebase app instance
_firebase_app = None

def initialize_firebase_app(credentials_file: str):
    """Initialize Firebase app once and reuse it"""
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    try:
        # Check if credentials file exists
        if not os.path.exists(credentials_file):
            print(f"❌ Credentials file not found: {credentials_file}")
            return None
        
        # Check if default app already exists
        try:
            _firebase_app = firebase_admin.get_app()
            print("✅ Using existing Firebase app")
        except ValueError:
            # Initialize new app
            cred = credentials.Certificate(credentials_file)
            _firebase_app = firebase_admin.initialize_app(cred)
            print("✅ Firebase app initialized successfully")
        
        return _firebase_app
        
    except Exception as e:
        print(f"❌ Failed to initialize Firebase app: {e}")
        return None

def test_firebase_connection(credentials_file: str):
    """Test Firebase connection with credentials file"""
    print(f"Testing Firebase connection with credentials: {credentials_file}")
    
    try:
        # Initialize Firebase app
        app = initialize_firebase_app(credentials_file)
        if not app:
            return False
        
        print("✅ Firebase connection successful")
        
        # Get project ID from credentials
        with open(credentials_file, 'r') as f:
            cred_data = json.load(f)
            project_id = cred_data.get('project_id', 'Unknown')
        
        print(f"   Project ID: {project_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test Firebase connection: {e}")
        return False

def test_notification_sending(credentials_file: str, topic: str = "test_topic", 
                            title: str = "Test Notification", 
                            body: str = "This is a test notification from Home-Vision-AI",
                            data: Dict[str, str] = None):
    """Test sending a notification to a topic"""
    print(f"\nTesting notification sending to topic: {topic}")
    print(f"Title: {title}")
    print(f"Body: {body}")
    
    try:
        # Get Firebase app
        app = initialize_firebase_app(credentials_file)
        if not app:
            return False
        
        # Prepare data payload
        if data is None:
            data = {
                "test": "true",
                "timestamp": str(int(time.time())),
                "source": "home-vision-ai"
            }
        
        # Create test message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data,
            topic=topic
        )
        
        # Send message
        response = messaging.send(message)
        print(f"✅ Notification sent successfully")
        print(f"   Message ID: {response}")
        print(f"   Topic: {topic}")
        print(f"   Data payload: {data}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

def test_detection_notification(credentials_file: str, camera_name: str = "Test Camera"):
    """Test sending a detection event notification"""
    print(f"\nTesting detection notification for camera: {camera_name}")
    
    title = f"Detection Alert - Cat"
    body = f"Cat detected on {camera_name} camera"
    
    data = {
        "event_id": "test_event_123",
        "camera_id": "1",
        "object_type": "cat",
        "confidence": "0.95",
        "timestamp": str(int(time.time())),
        "camera_name": camera_name
    }
    
    return test_notification_sending(
        credentials_file, 
        topic="detection_events",
        title=title,
        body=body,
        data=data
    )

def test_camera_status_notification(credentials_file: str, camera_name: str = "Test Camera", 
                                  status: str = "offline"):
    """Test sending a camera status notification"""
    print(f"\nTesting camera status notification for: {camera_name}")
    
    title = f"Camera Status - {camera_name}"
    body = f"Camera {camera_name} is now {status}"
    
    data = {
        "camera_name": camera_name,
        "status": status,
        "timestamp": str(int(time.time())),
        "type": "camera_status"
    }
    
    return test_notification_sending(
        credentials_file,
        topic="camera_status",
        title=title,
        body=body,
        data=data
    )

def test_system_notification(credentials_file: str, title: str = "System Alert", 
                           body: str = "System maintenance scheduled"):
    """Test sending a system notification"""
    print(f"\nTesting system notification")
    
    data = {
        "type": "system",
        "priority": "normal",
        "timestamp": str(int(time.time())),
        "source": "home-vision-ai"
    }
    
    return test_notification_sending(
        credentials_file,
        topic="system_notifications",
        title=title,
        body=body,
        data=data
    )

def test_topic_subscription(credentials_file: str, tokens: List[str], topic: str):
    """Test subscribing devices to a topic"""
    print(f"\nTesting topic subscription for topic: {topic}")
    print(f"Number of tokens: {len(tokens)}")
    
    try:
        # Get Firebase app
        app = initialize_firebase_app(credentials_file)
        if not app:
            return False
        
        # Subscribe to topic
        response = messaging.subscribe_to_topic(tokens, topic)
        print(f"✅ Topic subscription successful")
        print(f"   Success count: {response.success_count}")
        print(f"   Failure count: {response.failure_count}")
        
        if response.failure_count > 0:
            print(f"   Errors: {response.errors}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to subscribe to topic: {e}")
        return False

def test_topic_unsubscription(credentials_file: str, tokens: List[str], topic: str):
    """Test unsubscribing devices from a topic"""
    print(f"\nTesting topic unsubscription for topic: {topic}")
    print(f"Number of tokens: {len(tokens)}")
    
    try:
        # Get Firebase app
        app = initialize_firebase_app(credentials_file)
        if not app:
            return False
        
        # Unsubscribe from topic
        response = messaging.unsubscribe_from_topic(tokens, topic)
        print(f"✅ Topic unsubscription successful")
        print(f"   Success count: {response.success_count}")
        print(f"   Failure count: {response.failure_count}")
        
        if response.failure_count > 0:
            print(f"   Errors: {response.errors}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to unsubscribe from topic: {e}")
        return False

def run_comprehensive_tests(credentials_file: str):
    """Run a comprehensive set of notification tests"""
    print("Running comprehensive notification tests...")
    print("=" * 50)
    
    tests = [
        ("Basic Test Notification", lambda: test_notification_sending(credentials_file, "test_topic")),
        ("Detection Event Notification", lambda: test_detection_notification(credentials_file, "Front Door Camera")),
        ("Camera Status Notification", lambda: test_camera_status_notification(credentials_file, "Back Yard Camera", "online")),
        ("System Notification", lambda: test_system_notification(credentials_file, "System Alert", "AI model updated successfully")),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*30}")
        print(f"Running: {test_name}")
        print('='*30)
        
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results[test_name] = False
    
    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    return passed == total

def main():
    parser = argparse.ArgumentParser(description="Firebase Notification Test Tool")
    parser.add_argument("--credentials", default="backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json",
                       help="Path to Firebase credentials file")
    parser.add_argument("--test", choices=["connection", "basic", "detection", "status", "system", "comprehensive"],
                       help="Run specific test")
    parser.add_argument("--topic", default="test_topic", help="Topic for notifications")
    parser.add_argument("--title", help="Notification title")
    parser.add_argument("--body", help="Notification body")
    parser.add_argument("--camera", default="Test Camera", help="Camera name for status/detection tests")
    parser.add_argument("--status", choices=["online", "offline", "error"], default="offline", 
                       help="Camera status for status test")
    
    args = parser.parse_args()
    
    # Check if credentials file exists
    if not os.path.exists(args.credentials):
        print(f"❌ Credentials file not found: {args.credentials}")
        print("Please ensure your Firebase credentials file exists and is accessible.")
        sys.exit(1)
    
    print("Firebase Notification Test Tool")
    print("==============================")
    
    # Initialize Firebase app once
    if not initialize_firebase_app(args.credentials):
        print("❌ Firebase initialization failed. Please check your credentials file.")
        sys.exit(1)
    
    # Run specific test if requested
    if args.test:
        if args.test == "connection":
            print("✅ Connection test completed")
        elif args.test == "basic":
            title = args.title or "Test Notification"
            body = args.body or "This is a test notification from Home-Vision-AI"
            test_notification_sending(args.credentials, args.topic, title, body)
        elif args.test == "detection":
            test_detection_notification(args.credentials, args.camera)
        elif args.test == "status":
            test_camera_status_notification(args.credentials, args.camera, args.status)
        elif args.test == "system":
            title = args.title or "System Alert"
            body = args.body or "System maintenance scheduled"
            test_system_notification(args.credentials, title, body)
        elif args.test == "comprehensive":
            run_comprehensive_tests(args.credentials)
    else:
        # Interactive mode
        print("\nInteractive Testing Mode")
        print("======================")
        
    while True:
        print("\nOptions:")
            print("1. Send basic test notification")
            print("2. Send detection event notification")
            print("3. Send camera status notification")
            print("4. Send system notification")
            print("5. Subscribe devices to topic")
            print("6. Unsubscribe devices from topic")
            print("7. Run comprehensive tests")
            print("8. Exit")
        
            choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            topic = input("Enter topic name (default: test_topic): ").strip() or "test_topic"
                title = input("Enter notification title (default: Test Notification): ").strip() or "Test Notification"
                body = input("Enter notification body: ").strip() or "This is a test notification from Home-Vision-AI"
                test_notification_sending(args.credentials, topic, title, body)
            
        elif choice == "2":
                camera = input("Enter camera name (default: Test Camera): ").strip() or "Test Camera"
                test_detection_notification(args.credentials, camera)
                
            elif choice == "3":
                camera = input("Enter camera name (default: Test Camera): ").strip() or "Test Camera"
                status = input("Enter status (online/offline/error, default: offline): ").strip() or "offline"
                test_camera_status_notification(args.credentials, camera, status)
                
            elif choice == "4":
                title = input("Enter notification title (default: System Alert): ").strip() or "System Alert"
                body = input("Enter notification body: ").strip() or "System maintenance scheduled"
                test_system_notification(args.credentials, title, body)
                
            elif choice == "5":
            print("Enter device tokens (one per line, empty line to finish):")
            tokens = []
            while True:
                token = input("Token: ").strip()
                if not token:
                    break
                tokens.append(token)
            
            if tokens:
                topic = input("Enter topic name: ").strip()
                if topic:
                        test_topic_subscription(args.credentials, tokens, topic)
                    
            elif choice == "6":
                print("Enter device tokens (one per line, empty line to finish):")
                tokens = []
                while True:
                    token = input("Token: ").strip()
                    if not token:
                        break
                    tokens.append(token)
                
                if tokens:
                    topic = input("Enter topic name: ").strip()
            if topic:
                        test_topic_unsubscription(args.credentials, tokens, topic)
                        
            elif choice == "7":
                run_comprehensive_tests(args.credentials)
                
            elif choice == "8":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main() 