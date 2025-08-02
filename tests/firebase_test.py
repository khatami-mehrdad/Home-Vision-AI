#!/usr/bin/env python3
"""
Firebase Test Script
Tests Firebase Cloud Messaging connectivity and notification sending
"""

import firebase_admin
from firebase_admin import credentials, messaging
import json
import sys
import os

def test_firebase_connection(credentials_file: str):
    """Test Firebase connection with credentials file"""
    print(f"Testing Firebase connection with credentials: {credentials_file}")
    
    try:
        # Check if credentials file exists
        if not os.path.exists(credentials_file):
            print(f"❌ Credentials file not found: {credentials_file}")
            return False
        
        # Initialize Firebase with credentials
        cred = credentials.Certificate(credentials_file)
        app = firebase_admin.initialize_app(cred)
        
        print("✅ Firebase initialized successfully")
        
        # Get project ID from credentials
        with open(credentials_file, 'r') as f:
            cred_data = json.load(f)
            project_id = cred_data.get('project_id', 'Unknown')
        
        print(f"   Project ID: {project_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize Firebase: {e}")
        return False

def test_notification_sending(credentials_file: str, topic: str = "test_topic"):
    """Test sending a notification to a topic"""
    print(f"\nTesting notification sending to topic: {topic}")
    
    try:
        # Initialize Firebase
        cred = credentials.Certificate(credentials_file)
        app = firebase_admin.initialize_app(cred)
        
        # Create test message
        message = messaging.Message(
            notification=messaging.Notification(
                title="Test Notification",
                body="This is a test notification from Home-Vision-AI"
            ),
            data={
                "test": "true",
                "timestamp": str(int(time.time()))
            },
            topic=topic
        )
        
        # Send message
        response = messaging.send(message)
        print(f"✅ Notification sent successfully")
        print(f"   Message ID: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        return False

def test_topic_subscription(credentials_file: str, tokens: list, topic: str):
    """Test subscribing devices to a topic"""
    print(f"\nTesting topic subscription for topic: {topic}")
    
    try:
        # Initialize Firebase
        cred = credentials.Certificate(credentials_file)
        app = firebase_admin.initialize_app(cred)
        
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

def main():
    # Default credentials file path
    credentials_file = "backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json"
    
    print("Firebase Test Tool")
    print("==================")
    
    # Test 1: Connection
    print("\n1. Testing Firebase Connection")
    connection_success = test_firebase_connection(credentials_file)
    
    if not connection_success:
        print("❌ Firebase connection failed. Please check your credentials file.")
        sys.exit(1)
    
    # Test 2: Notification Sending
    print("\n2. Testing Notification Sending")
    notification_success = test_notification_sending(credentials_file, "test_topic")
    
    # Test 3: Interactive mode
    print("\n3. Interactive Testing")
    while True:
        print("\nOptions:")
        print("1. Send test notification")
        print("2. Subscribe devices to topic")
        print("3. Test with custom topic")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            topic = input("Enter topic name (default: test_topic): ").strip() or "test_topic"
            test_notification_sending(credentials_file, topic)
            
        elif choice == "2":
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
                    test_topic_subscription(credentials_file, tokens, topic)
                    
        elif choice == "3":
            topic = input("Enter custom topic name: ").strip()
            if topic:
                test_notification_sending(credentials_file, topic)
                
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    import time
    main() 