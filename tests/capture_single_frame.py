#!/usr/bin/env python3
"""
Simple Frame Capture Script
Captures a single frame from camera for testing
"""

import cv2
import numpy as np
import requests
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def capture_direct_frame(rtsp_url: str, output_path: str = "single_frame.jpg"):
    """Capture a single frame directly from RTSP stream"""
    logger.info(f"Capturing frame from: {rtsp_url}")
    
    try:
        cap = cv2.VideoCapture(rtsp_url)
        
        if not cap.isOpened():
            logger.error("Failed to open camera stream")
            return False
        
        logger.info("Camera stream opened successfully")
        
        # Read one frame
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to read frame from camera")
            cap.release()
            return False
        
        logger.info(f"Successfully read frame: {frame.shape}")
        
        # Save the frame
        cv2.imwrite(output_path, frame)
        logger.info(f"Saved frame to: {output_path}")
        
        cap.release()
        return True
        
    except Exception as e:
        logger.error(f"Error capturing frame: {e}")
        return False

def capture_api_frame(camera_id: int = 1, output_path: str = "api_frame.jpg"):
    """Capture a single frame via API"""
    logger.info(f"Capturing frame via API for camera {camera_id}")
    
    try:
        # Start camera stream
        response = requests.post(f"http://localhost:8000/api/v1/cameras/{camera_id}/start", timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to start camera stream: {response.status_code}")
            return False
        
        logger.info("Camera stream started via API")
        
        # Wait a bit for stream to initialize
        time.sleep(2)
        
        # Get a frame
        response = requests.get(f"http://localhost:8000/api/v1/cameras/{camera_id}/frame", timeout=10)
        if response.status_code == 200:
            # Save the frame
            with open(output_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"Frame captured via API: {output_path}")
            return True
        else:
            logger.error(f"Failed to get frame: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error capturing frame via API: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Capture Single Frame")
    parser.add_argument("--rtsp-url", help="RTSP URL for direct capture")
    parser.add_argument("--camera-id", type=int, default=1, help="Camera ID for API capture")
    parser.add_argument("--method", choices=["direct", "api", "both"], default="both", 
                       help="Capture method to use")
    
    args = parser.parse_args()
    
    if args.method in ["direct", "both"]:
        if not args.rtsp_url:
            logger.error("RTSP URL required for direct capture")
            return 1
        
        logger.info("=" * 40)
        logger.info("DIRECT FRAME CAPTURE")
        logger.info("=" * 40)
        success = capture_direct_frame(args.rtsp_url, "direct_frame.jpg")
        logger.info(f"Direct capture: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    if args.method in ["api", "both"]:
        logger.info("=" * 40)
        logger.info("API FRAME CAPTURE")
        logger.info("=" * 40)
        success = capture_api_frame(args.camera_id, "api_frame.jpg")
        logger.info(f"API capture: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Check results
    import os
    logger.info("\n" + "=" * 40)
    logger.info("CAPTURED FRAMES")
    logger.info("=" * 40)
    
    for frame_file in ["direct_frame.jpg", "api_frame.jpg"]:
        if os.path.exists(frame_file):
            size = os.path.getsize(frame_file)
            logger.info(f"✅ {frame_file}: {size} bytes")
        else:
            logger.info(f"❌ {frame_file}: Not found")
    
    return 0

if __name__ == "__main__":
    exit(main()) 