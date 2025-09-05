#!/usr/bin/env python3
"""
Quick RTSP connection test script
"""
import cv2
import sys
import json
import time

def test_rtsp_connection(rtsp_url):
    """Test RTSP connection and capture a few frames"""
    print(f"🔍 Testing RTSP connection: {rtsp_url}")
    
    try:
        # Open the RTSP stream
        print("📹 Opening video capture...")
        cap = cv2.VideoCapture(rtsp_url)
        
        if not cap.isOpened():
            print("❌ Failed to open RTSP stream")
            return False
            
        print("✅ RTSP stream opened successfully")
        
        # Get stream properties
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"📊 Stream properties: {width}x{height} @ {fps} FPS")
        
        # Try to read a few frames
        frame_count = 0
        success_count = 0
        start_time = time.time()
        
        for i in range(10):
            ret, frame = cap.read()
            frame_count += 1
            
            if ret and frame is not None:
                success_count += 1
                print(f"✅ Frame {i+1}: {frame.shape} - OK")
            else:
                print(f"❌ Frame {i+1}: Failed to read")
            
            time.sleep(0.1)  # Small delay between frames
        
        elapsed_time = time.time() - start_time
        print(f"📈 Results: {success_count}/{frame_count} frames successful in {elapsed_time:.2f}s")
        
        cap.release()
        
        return success_count > 0
        
    except Exception as e:
        print(f"💥 Exception during RTSP test: {e}")
        return False

def load_camera_config():
    """Load camera configuration"""
    try:
        with open('../camera_config.json', 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Failed to load camera config: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Home Vision AI - RTSP Connection Test")
    print("=" * 50)
    
    # Load camera config
    config = load_camera_config()
    if not config:
        print("❌ Cannot proceed without camera configuration")
        sys.exit(1)
    
    # Test each camera
    cameras = config.get('cameras', [])
    if not cameras:
        print("❌ No cameras found in configuration")
        sys.exit(1)
    
    print(f"📋 Found {len(cameras)} camera(s) to test")
    
    for camera in cameras:
        print(f"\n🎥 Testing Camera: {camera['name']}")
        print(f"📍 Location: {camera.get('location', 'Unknown')}")
        print(f"🔗 RTSP URL: {camera['rtsp_url']}")
        
        success = test_rtsp_connection(camera['rtsp_url'])
        
        if success:
            print(f"✅ Camera '{camera['name']}' test PASSED")
        else:
            print(f"❌ Camera '{camera['name']}' test FAILED")
        
        print("-" * 30)
    
    print("\n🏁 RTSP test completed")
