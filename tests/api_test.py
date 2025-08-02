#!/usr/bin/env python3
"""
FastAPI Backend Test Script
Tests the Home-Vision-AI API endpoints
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    def test_health_endpoint(self) -> bool:
        """Test the health check endpoint"""
        print("Testing health endpoint...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Health endpoint error: {e}")
            return False
    
    def test_api_docs(self) -> bool:
        """Test API documentation endpoint"""
        print("\nTesting API documentation...")
        
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ API documentation accessible")
                return True
            else:
                print(f"❌ API documentation failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API documentation error: {e}")
            return False
    
    def test_cameras_endpoint(self) -> bool:
        """Test cameras endpoint"""
        print("\nTesting cameras endpoint...")
        
        try:
            response = requests.get(f"{self.api_url}/cameras", timeout=10)
            if response.status_code == 200:
                cameras = response.json()
                print("✅ Cameras endpoint working")
                print(f"   Found {len(cameras)} cameras")
                for camera in cameras:
                    print(f"   - {camera.get('name', 'Unknown')}: {camera.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ Cameras endpoint failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cameras endpoint error: {e}")
            return False
    
    def test_camera_status(self) -> bool:
        """Test camera status endpoint"""
        print("\nTesting camera status endpoint...")
        
        try:
            response = requests.get(f"{self.api_url}/cameras/status/all", timeout=10)
            if response.status_code == 200:
                statuses = response.json()
                print("✅ Camera status endpoint working")
                print(f"   Active cameras: {len(statuses)}")
                for camera_id, status in statuses.items():
                    streaming = "🟢" if status.get('is_streaming') else "🔴"
                    print(f"   {streaming} Camera {camera_id}: {'Streaming' if status.get('is_streaming') else 'Offline'}")
                return True
            else:
                print(f"❌ Camera status endpoint failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Camera status endpoint error: {e}")
            return False
    
    def test_events_endpoint(self) -> bool:
        """Test events endpoint"""
        print("\nTesting events endpoint...")
        
        try:
            response = requests.get(f"{self.api_url}/events", timeout=10)
            if response.status_code == 200:
                events = response.json()
                print("✅ Events endpoint working")
                print(f"   Found {len(events)} events")
                return True
            else:
                print(f"❌ Events endpoint failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Events endpoint error: {e}")
            return False
    
    def test_notifications_endpoint(self) -> bool:
        """Test notifications endpoint"""
        print("\nTesting notifications endpoint...")
        
        try:
            response = requests.get(f"{self.api_url}/notifications", timeout=10)
            if response.status_code == 200:
                notifications = response.json()
                print("✅ Notifications endpoint working")
                print(f"   Found {len(notifications)} notifications")
                return True
            else:
                print(f"❌ Notifications endpoint failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Notifications endpoint error: {e}")
            return False
    
    def test_camera_frame(self, camera_id: int = 1) -> bool:
        """Test camera frame endpoint"""
        print(f"\nTesting camera frame endpoint for camera {camera_id}...")
        
        try:
            response = requests.get(f"{self.api_url}/cameras/{camera_id}/frame", timeout=10)
            if response.status_code == 200:
                print("✅ Camera frame endpoint working")
                print(f"   Frame size: {len(response.content)} bytes")
                print(f"   Content type: {response.headers.get('content-type', 'Unknown')}")
                return True
            elif response.status_code == 404:
                print("⚠️  Camera frame not available (camera may be offline)")
                return True  # This is expected if camera is not streaming
            else:
                print(f"❌ Camera frame endpoint failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Camera frame endpoint error: {e}")
            return False
    
    def test_create_camera(self) -> bool:
        """Test creating a camera"""
        print("\nTesting camera creation...")
        
        camera_data = {
            "name": "Test Camera",
            "rtsp_url": "rtsp://192.168.1.100:554/stream1",
            "location": "Test Location",
            "frame_rate": 10,
            "resolution": "1080p",
            "detection_enabled": True
        }
        
        try:
            response = requests.post(f"{self.api_url}/cameras", json=camera_data, timeout=10)
            if response.status_code == 200:
                camera = response.json()
                print("✅ Camera creation working")
                print(f"   Created camera: {camera.get('name')} (ID: {camera.get('id')})")
                return True
            else:
                print(f"❌ Camera creation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Camera creation error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all API tests"""
        print("Home-Vision-AI API Test Suite")
        print("=============================")
        
        tests = {
            "Health Check": self.test_health_endpoint,
            "API Documentation": self.test_api_docs,
            "Cameras Endpoint": self.test_cameras_endpoint,
            "Camera Status": self.test_camera_status,
            "Events Endpoint": self.test_events_endpoint,
            "Notifications Endpoint": self.test_notifications_endpoint,
            "Camera Frame": self.test_camera_frame,
            "Camera Creation": self.test_create_camera,
        }
        
        results = {}
        
        for test_name, test_func in tests.items():
            print(f"\n{'='*50}")
            print(f"Running: {test_name}")
            print('='*50)
            
            try:
                success = test_func()
                results[test_name] = success
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                results[test_name] = False
        
        return results
    
    def print_summary(self, results: Dict[str, bool]):
        """Print test results summary"""
        print(f"\n{'='*50}")
        print("TEST RESULTS SUMMARY")
        print('='*50)
        
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the logs above.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Home-Vision-AI API Test Tool")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Base URL of the API server")
    parser.add_argument("--test", choices=["health", "cameras", "events", "notifications", "all"],
                       default="all", help="Specific test to run")
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    
    if args.test == "all":
        results = tester.run_all_tests()
        tester.print_summary(results)
        
        # Exit with appropriate code
        all_passed = all(results.values())
        sys.exit(0 if all_passed else 1)
        
    elif args.test == "health":
        success = tester.test_health_endpoint()
        sys.exit(0 if success else 1)
        
    elif args.test == "cameras":
        success = tester.test_cameras_endpoint() and tester.test_camera_status()
        sys.exit(0 if success else 1)
        
    elif args.test == "events":
        success = tester.test_events_endpoint()
        sys.exit(0 if success else 1)
        
    elif args.test == "notifications":
        success = tester.test_notifications_endpoint()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 