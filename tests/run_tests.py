#!/usr/bin/env python3
"""
Home-Vision-AI Test Suite Runner
Runs all tests to verify system components
"""

import subprocess
import sys
import os
import time
import argparse
from typing import Dict, List, Tuple

class TestRunner:
    def __init__(self):
        self.test_results: Dict[str, bool] = {}
        self.test_outputs: Dict[str, str] = {}
        
    def run_command(self, command: List[str], timeout: int = 60) -> Tuple[bool, str]:
        """Run a command and return success status and output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            success = result.returncode == 0
            output = result.stdout + result.stderr
            return success, output
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, f"Command failed: {e}"
    
    def test_rtsp_cameras(self) -> bool:
        """Test RTSP camera connectivity"""
        print("🔍 Testing RTSP Camera Connectivity")
        print("=" * 50)
        
        # Check if OpenCV is available
        try:
            import cv2
            print("✅ OpenCV is available")
        except ImportError:
            print("❌ OpenCV not available. Install with: pip install opencv-python")
            return False
        
        # Run RTSP test
        success, output = self.run_command([
            sys.executable, "tests/rtsp_test.py", "--url", "rtsp://192.168.1.100:554/stream1"
        ])
        
        if success:
            print("✅ RTSP test passed")
        else:
            print("❌ RTSP test failed")
            print("   Note: This is expected if no cameras are configured")
        
        print(output)
        return success
    
    def test_firebase_connection(self) -> bool:
        """Test Firebase connectivity"""
        print("\n🔥 Testing Firebase Connection")
        print("=" * 50)
        
        # Check if Firebase credentials exist
        creds_file = "backend/app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json"
        if not os.path.exists(creds_file):
            print(f"❌ Firebase credentials file not found: {creds_file}")
            return False
        
        print(f"✅ Firebase credentials found: {creds_file}")
        
        # Run Firebase test
        success, output = self.run_command([
            sys.executable, "tests/firebase_test.py"
        ])
        
        if success:
            print("✅ Firebase test passed")
        else:
            print("❌ Firebase test failed")
        
        print(output)
        return success
    
    def test_backend_api(self) -> bool:
        """Test FastAPI backend"""
        print("\n🚀 Testing FastAPI Backend")
        print("=" * 50)
        
        # Check if backend is running
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running")
            else:
                print("❌ Backend is not responding correctly")
                return False
        except requests.exceptions.RequestException:
            print("❌ Backend is not running. Start with: docker-compose up backend")
            return False
        
        # Run API tests
        success, output = self.run_command([
            sys.executable, "tests/api_test.py", "--test", "all"
        ])
        
        if success:
            print("✅ API tests passed")
        else:
            print("❌ API tests failed")
        
        print(output)
        return success
    
    def test_frontend(self) -> bool:
        """Test React frontend"""
        print("\n⚛️  Testing React Frontend")
        print("=" * 50)
        
        # Check if frontend dependencies are installed
        if not os.path.exists("frontend/node_modules"):
            print("❌ Frontend dependencies not installed. Run: cd frontend && npm install")
            return False
        
        print("✅ Frontend dependencies found")
        
        # Check if frontend is running
        try:
            import requests
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend is running")
                return True
            else:
                print("❌ Frontend is not responding correctly")
                return False
        except requests.exceptions.RequestException:
            print("❌ Frontend is not running. Start with: docker-compose up frontend")
            return False
    
    def test_docker_services(self) -> bool:
        """Test Docker services"""
        print("\n🐳 Testing Docker Services")
        print("=" * 50)
        
        # Check if Docker is running
        success, output = self.run_command(["docker", "info"])
        if not success:
            print("❌ Docker is not running")
            return False
        
        print("✅ Docker is running")
        
        # Check if services are running
        success, output = self.run_command(["docker-compose", "ps"])
        if success:
            print("✅ Docker services status:")
            print(output)
            return True
        else:
            print("❌ Failed to check Docker services")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests"""
        print("Home-Vision-AI Test Suite")
        print("========================")
        print(f"Running tests at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        tests = [
            ("Docker Services", self.test_docker_services),
            ("Firebase Connection", self.test_firebase_connection),
            ("Backend API", self.test_backend_api),
            ("Frontend", self.test_frontend),
            ("RTSP Cameras", self.test_rtsp_cameras),
        ]
        
        for test_name, test_func in tests:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print('='*60)
            
            try:
                success = test_func()
                self.test_results[test_name] = success
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                self.test_results[test_name] = False
        
        return self.test_results
    
    def print_summary(self):
        """Print test results summary"""
        print(f"\n{'='*60}")
        print("TEST RESULTS SUMMARY")
        print('='*60)
        
        passed = sum(1 for success in self.test_results.values() if success)
        total = len(self.test_results)
        
        for test_name, success in self.test_results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your Home-Vision-AI system is ready!")
        else:
            print("⚠️  Some tests failed. Check the logs above for details.")
            print("\nNext steps:")
            print("1. Fix any failed tests")
            print("2. Start services: docker-compose up")
            print("3. Access web interface: http://localhost:3000")
    
    def run_specific_test(self, test_name: str) -> bool:
        """Run a specific test"""
        test_map = {
            "docker": self.test_docker_services,
            "firebase": self.test_firebase_connection,
            "backend": self.test_backend_api,
            "frontend": self.test_frontend,
            "rtsp": self.test_rtsp_cameras,
        }
        
        if test_name not in test_map:
            print(f"❌ Unknown test: {test_name}")
            print(f"Available tests: {', '.join(test_map.keys())}")
            return False
        
        print(f"Running test: {test_name}")
        success = test_map[test_name]()
        
        if success:
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
        
        return success

def main():
    parser = argparse.ArgumentParser(description="Home-Vision-AI Test Suite")
    parser.add_argument("--test", choices=["docker", "firebase", "backend", "frontend", "rtsp", "all"],
                       default="all", help="Specific test to run")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.test == "all":
        results = runner.run_all_tests()
        runner.print_summary()
        
        # Exit with appropriate code
        all_passed = all(results.values())
        sys.exit(0 if all_passed else 1)
    else:
        success = runner.run_specific_test(args.test)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 