#!/usr/bin/env python3
"""
RTSP Camera Test Script
Tests RTSP camera connectivity and displays video feeds
"""

import cv2
import argparse
import sys
import time
from typing import Dict, Optional
import threading
import numpy as np

class RTSPCameraTest:
    def __init__(self):
        self.cameras: Dict[str, cv2.VideoCapture] = {}
        self.running = False
        
    def test_single_camera(self, rtsp_url: str, camera_name: str = "Camera") -> bool:
        """Test a single RTSP camera connection"""
        print(f"Testing camera: {camera_name}")
        print(f"RTSP URL: {rtsp_url}")
        
        try:
            # Create video capture object
            cap = cv2.VideoCapture(rtsp_url)
            
            if not cap.isOpened():
                print(f"❌ Failed to open camera: {camera_name}")
                return False
            
            # Set camera properties
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            cap.set(cv2.CAP_PROP_FPS, 10)
            
            # Try to read a frame
            ret, frame = cap.read()
            if not ret:
                print(f"❌ Failed to read frame from camera: {camera_name}")
                cap.release()
                return False
            
            print(f"✅ Successfully connected to camera: {camera_name}")
            print(f"   Frame size: {frame.shape}")
            print(f"   FPS: {cap.get(cv2.CAP_PROP_FPS)}")
            
            cap.release()
            return True
            
        except Exception as e:
            print(f"❌ Error testing camera {camera_name}: {e}")
            return False
    
    def display_camera_feed(self, rtsp_url: str, camera_name: str = "Camera", duration: int = 30):
        """Display camera feed for a specified duration"""
        print(f"Displaying feed from: {camera_name}")
        print(f"Duration: {duration} seconds")
        print("Press 'q' to quit early")
        
        cap = cv2.VideoCapture(rtsp_url)
        
        if not cap.isOpened():
            print(f"❌ Failed to open camera: {camera_name}")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FPS, 10)
        
        start_time = time.time()
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Failed to read frame")
                    break
                
                # Add info overlay
                elapsed = time.time() - start_time
                fps = frame_count / elapsed if elapsed > 0 else 0
                
                # Add text overlay
                cv2.putText(frame, f"{camera_name} - FPS: {fps:.1f}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Time: {elapsed:.1f}s", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Display frame
                cv2.imshow(camera_name, frame)
                frame_count += 1
                
                # Check for quit or timeout
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or elapsed >= duration:
                    break
                    
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            
        print(f"Displayed {frame_count} frames over {elapsed:.1f} seconds")
    
    def test_multiple_cameras(self, camera_configs: Dict[str, str]):
        """Test multiple cameras simultaneously"""
        print("Testing multiple cameras...")
        
        results = {}
        for camera_name, rtsp_url in camera_configs.items():
            success = self.test_single_camera(rtsp_url, camera_name)
            results[camera_name] = success
            
        print("\n=== Test Results ===")
        for camera_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{camera_name}: {status}")
        
        return results
    
    def display_multiple_feeds(self, camera_configs: Dict[str, str], duration: int = 30):
        """Display multiple camera feeds in separate windows"""
        print("Displaying multiple camera feeds...")
        
        # Start threads for each camera
        threads = []
        for camera_name, rtsp_url in camera_configs.items():
            thread = threading.Thread(
                target=self.display_camera_feed,
                args=(rtsp_url, camera_name, duration)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print("All camera feeds completed")

def main():
    parser = argparse.ArgumentParser(description="RTSP Camera Test Tool")
    parser.add_argument("--url", help="Single RTSP URL to test")
    parser.add_argument("--name", default="Camera", help="Camera name")
    parser.add_argument("--display", action="store_true", help="Display video feed")
    parser.add_argument("--duration", type=int, default=30, help="Display duration in seconds")
    parser.add_argument("--config", help="JSON file with multiple camera configurations")
    
    args = parser.parse_args()
    
    tester = RTSPCameraTest()
    
    if args.url:
        # Test single camera
        if args.display:
            tester.display_camera_feed(args.url, args.name, args.duration)
        else:
            success = tester.test_single_camera(args.url, args.name)
            sys.exit(0 if success else 1)
    
    elif args.config:
        # Test multiple cameras from config file
        import json
        try:
            with open(args.config, 'r') as f:
                camera_configs = json.load(f)
            
            if args.display:
                tester.display_multiple_feeds(camera_configs, args.duration)
            else:
                results = tester.test_multiple_cameras(camera_configs)
                all_passed = all(results.values())
                sys.exit(0 if all_passed else 1)
                
        except FileNotFoundError:
            print(f"❌ Config file not found: {args.config}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in config file: {args.config}")
            sys.exit(1)
    
    else:
        # Interactive mode
        print("RTSP Camera Test Tool")
        print("====================")
        
        while True:
            print("\nOptions:")
            print("1. Test single camera")
            print("2. Test multiple cameras")
            print("3. Display camera feed")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                url = input("Enter RTSP URL: ").strip()
                name = input("Enter camera name (optional): ").strip() or "Camera"
                success = tester.test_single_camera(url, name)
                print("✅ Test passed" if success else "❌ Test failed")
                
            elif choice == "2":
                print("Enter camera configurations (name:url format)")
                print("Press Enter twice to finish")
                camera_configs = {}
                while True:
                    line = input("Camera (name:url): ").strip()
                    if not line:
                        break
                    if ":" in line:
                        name, url = line.split(":", 1)
                        camera_configs[name.strip()] = url.strip()
                
                if camera_configs:
                    results = tester.test_multiple_cameras(camera_configs)
                    all_passed = all(results.values())
                    print("✅ All tests passed" if all_passed else "❌ Some tests failed")
                
            elif choice == "3":
                url = input("Enter RTSP URL: ").strip()
                name = input("Enter camera name (optional): ").strip() or "Camera"
                duration = input("Enter duration in seconds (default 30): ").strip()
                duration = int(duration) if duration.isdigit() else 30
                tester.display_camera_feed(url, name, duration)
                
            elif choice == "4":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 