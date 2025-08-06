#!/usr/bin/env python3
"""
Camera Integration Test Script
Tests camera service, API endpoints, and frame capture
"""

import asyncio
import cv2
import numpy as np
import requests
import json
import time
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CameraIntegrationTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    def test_direct_camera_connection(self, rtsp_url: str) -> bool:
        """Test direct OpenCV connection to camera"""
        logger.info(f"Testing direct camera connection: {rtsp_url}")
        
        try:
            cap = cv2.VideoCapture(rtsp_url)
            
            if not cap.isOpened():
                logger.error("Failed to open camera stream")
                return False
            
            logger.info("Camera stream opened successfully")
            
            # Try to read one frame
            ret, frame = cap.read()
            if not ret:
                logger.error("Failed to read frame from camera")
                cap.release()
                return False
            
            logger.info(f"Successfully read frame: {frame.shape}")
            
            # Save the frame
            output_path = "test_direct_frame.jpg"
            cv2.imwrite(output_path, frame)
            logger.info(f"Saved frame to: {output_path}")
            
            cap.release()
            return True
            
        except Exception as e:
            logger.error(f"Error testing direct camera connection: {e}")
            return False
    
    def test_camera_service(self, rtsp_url: str, camera_name: str = "Test Camera") -> bool:
        """Test the camera service integration"""
        logger.info(f"Testing camera service with: {rtsp_url}")
        
        try:
            # Import camera service
            import sys
            sys.path.append('backend')
            from app.services.camera_service import camera_service
            from app.models.camera import Camera
            
            async def test_service():
                camera = Camera(
                    id=1,
                    name=camera_name,
                    rtsp_url=rtsp_url,
                    frame_rate=10
                )
                
                logger.info("Starting camera stream via service...")
                success = await camera_service.start_camera_stream(camera)
                logger.info(f"Stream started: {success}")
                
                if success:
                    # Wait a bit for frames to be captured
                    await asyncio.sleep(3)
                    
                    # Try to get a frame
                    frame_bytes = camera_service.get_latest_frame(1)
                    logger.info(f"Frame available: {frame_bytes is not None}")
                    
                    if frame_bytes:
                        logger.info(f"Frame size: {len(frame_bytes)} bytes")
                        
                        # Convert bytes to image and save
                        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
                        frame_img = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                        
                        output_path = "test_service_frame.jpg"
                        cv2.imwrite(output_path, frame_img)
                        logger.info(f"Saved service frame to: {output_path}")
                        
                        return True
                    else:
                        logger.error("No frame available from service")
                        return False
                else:
                    logger.error("Failed to start camera stream")
                    return False
            
            return asyncio.run(test_service())
            
        except Exception as e:
            logger.error(f"Error testing camera service: {e}")
            return False
    
    def test_api_endpoints(self) -> bool:
        """Test API endpoints"""
        logger.info("Testing API endpoints...")
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Health endpoint working")
            else:
                logger.error(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test cameras endpoint
            response = requests.get(f"{self.api_url}/cameras/", timeout=10)
            if response.status_code == 200:
                cameras = response.json()
                logger.info(f"✅ Cameras endpoint working - Found {len(cameras)} cameras")
                for camera in cameras:
                    logger.info(f"   Camera: {camera['name']} - {camera['rtsp_url']}")
            else:
                logger.error(f"❌ Cameras endpoint failed: {response.status_code}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error testing API endpoints: {e}")
            return False
    
    def test_camera_stream_api(self, camera_id: int = 1) -> bool:
        """Test camera stream via API"""
        logger.info(f"Testing camera stream API for camera {camera_id}")
        
        try:
            # Start camera stream
            response = requests.post(f"{self.api_url}/cameras/{camera_id}/start", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Camera stream started via API")
            else:
                logger.error(f"❌ Failed to start camera stream: {response.status_code}")
                return False
            
            # Wait a bit for stream to initialize
            time.sleep(2)
            
            # Get a frame
            response = requests.get(f"{self.api_url}/cameras/{camera_id}/frame", timeout=10)
            if response.status_code == 200:
                # Save the frame
                output_path = f"test_api_frame_{camera_id}.jpg"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"✅ Frame captured via API: {output_path}")
                return True
            else:
                logger.error(f"❌ Failed to get frame: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error testing camera stream API: {e}")
            return False
    
    def run_all_tests(self, rtsp_url: str, camera_name: str = "Test Camera"):
        """Run all camera integration tests"""
        logger.info("=" * 50)
        logger.info("CAMERA INTEGRATION TESTS")
        logger.info("=" * 50)
        
        results = {}
        
        # Test 1: Direct camera connection
        logger.info("\n1. Testing direct camera connection...")
        results['direct_connection'] = self.test_direct_camera_connection(rtsp_url)
        
        # Test 2: API endpoints
        logger.info("\n2. Testing API endpoints...")
        results['api_endpoints'] = self.test_api_endpoints()
        
        # Test 3: Camera service
        logger.info("\n3. Testing camera service...")
        results['camera_service'] = self.test_camera_service(rtsp_url, camera_name)
        
        # Test 4: Camera stream API
        logger.info("\n4. Testing camera stream API...")
        results['camera_stream_api'] = self.test_camera_stream_api()
        
        # Print results
        logger.info("\n" + "=" * 50)
        logger.info("TEST RESULTS")
        logger.info("=" * 50)
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
        
        passed = sum(results.values())
        total = len(results)
        logger.info(f"\nOverall: {passed}/{total} tests passed")
        
        return passed == total

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Camera Integration Test")
    parser.add_argument("--rtsp-url", required=True, help="RTSP URL to test")
    parser.add_argument("--camera-name", default="Test Camera", help="Camera name")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    
    args = parser.parse_args()
    
    tester = CameraIntegrationTest(args.api_url)
    success = tester.run_all_tests(args.rtsp_url, args.camera_name)
    
    if success:
        logger.info("🎉 All tests passed!")
    else:
        logger.error("❌ Some tests failed")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 