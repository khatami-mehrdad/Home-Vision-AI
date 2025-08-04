#!/usr/bin/env python3
"""
RTSP Camera Test Script
Tests RTSP camera connectivity and displays video feeds
Supports headless mode for remote SSH sessions
"""

import cv2
import argparse
import sys
import time
import os
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
    
    def create_video_from_frames(self, frames_dir: str, output_video: str, fps: int = 10):
        """Create a video from saved frames"""
        print(f"Creating video from frames in: {frames_dir}")
        print(f"Output video: {output_video}")
        print(f"Target FPS: {fps}")
        
        # Get all frame files
        frame_files = []
        for file in os.listdir(frames_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                frame_files.append(os.path.join(frames_dir, file))
        
        if not frame_files:
            print("❌ No frame files found")
            return False
        
        # Sort frame files by name (which should include frame numbers)
        frame_files.sort()
        
        # Read first frame to get dimensions
        first_frame = cv2.imread(frame_files[0])
        if first_frame is None:
            print("❌ Could not read first frame")
            return False
        
        height, width, layers = first_frame.shape
        print(f"Video dimensions: {width}x{height}")
        print(f"Total frames: {len(frame_files)}")
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID' for .avi
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        
        if not video_writer.isOpened():
            print("❌ Could not create video writer")
            return False
        
        # Process each frame
        for i, frame_file in enumerate(frame_files):
            frame = cv2.imread(frame_file)
            if frame is not None:
                video_writer.write(frame)
                if i % 10 == 0:  # Progress update every 10 frames
                    print(f"Processing frame {i+1}/{len(frame_files)}")
            else:
                print(f"Warning: Could not read frame {frame_file}")
        
        video_writer.release()
        print(f"✅ Video created successfully: {output_video}")
        print(f"   Duration: {len(frame_files)/fps:.1f} seconds")
        return True
    
    def display_camera_feed(self, rtsp_url: str, camera_name: str = "Camera", duration: int = 30, 
                           headless: bool = False, save_frames: bool = False, output_dir: str = "frames",
                           create_video: bool = False, video_fps: int = 10):
        """Display camera feed for a specified duration"""
        print(f"Displaying feed from: {camera_name}")
        print(f"Duration: {duration} seconds")
        
        if headless:
            print("Running in headless mode - no GUI windows")
            if save_frames:
                os.makedirs(output_dir, exist_ok=True)
                print(f"Saving frames to: {output_dir}")
                if create_video:
                    print(f"Will create video with {video_fps} FPS")
        else:
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
                
                if headless:
                    # In headless mode, just save frames or print status
                    if save_frames and frame_count % 10 == 0:  # Save every 10th frame
                        frame_path = os.path.join(output_dir, f"{camera_name}_{frame_count:06d}.jpg")
                        cv2.imwrite(frame_path, frame)
                        print(f"Saved frame {frame_count} to {frame_path}")
                    
                    # Print status every second
                    if frame_count % 10 == 0:
                        print(f"Frame {frame_count}, FPS: {fps:.1f}, Time: {elapsed:.1f}s")
                else:
                    # Display frame in GUI window
                    cv2.imshow(camera_name, frame)
                
                frame_count += 1
                
                # Check for quit or timeout
                if not headless:
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                
                if elapsed >= duration:
                    break
                    
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cap.release()
            if not headless:
                cv2.destroyAllWindows()
            
        print(f"Displayed {frame_count} frames over {elapsed:.1f} seconds")
        if save_frames:
            print(f"Frames saved to: {output_dir}")
            
            # Create video from frames if requested
            if create_video and save_frames:
                video_filename = f"{camera_name}_video.mp4"
                self.create_video_from_frames(output_dir, video_filename, video_fps)
    
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
    
    def display_multiple_feeds(self, camera_configs: Dict[str, str], duration: int = 30,
                             headless: bool = False, save_frames: bool = False, output_dir: str = "frames",
                             create_video: bool = False, video_fps: int = 10):
        """Display multiple camera feeds in separate windows"""
        print("Displaying multiple camera feeds...")
        
        # Start threads for each camera
        threads = []
        for camera_name, rtsp_url in camera_configs.items():
            camera_output_dir = os.path.join(output_dir, camera_name) if save_frames else output_dir
            thread = threading.Thread(
                target=self.display_camera_feed,
                args=(rtsp_url, camera_name, duration, headless, save_frames, camera_output_dir, create_video, video_fps)
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
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (no GUI)")
    parser.add_argument("--save-frames", action="store_true", help="Save frames to files (headless mode)")
    parser.add_argument("--output-dir", default="frames", help="Output directory for saved frames")
    parser.add_argument("--create-video", action="store_true", help="Create video from saved frames")
    parser.add_argument("--video-fps", type=int, default=10, help="FPS for created video")
    parser.add_argument("--frames-to-video", help="Create video from existing frames directory")
    parser.add_argument("--video-output", help="Output video filename")
    
    args = parser.parse_args()
    
    tester = RTSPCameraTest()
    
    # Handle frames-to-video conversion
    if args.frames_to_video:
        output_video = args.video_output or "output_video.mp4"
        success = tester.create_video_from_frames(args.frames_to_video, output_video, args.video_fps)
        sys.exit(0 if success else 1)
    
    if args.url:
        # Test single camera
        if args.display:
            tester.display_camera_feed(args.url, args.name, args.duration, 
                                    args.headless, args.save_frames, args.output_dir,
                                    args.create_video, args.video_fps)
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
                tester.display_multiple_feeds(camera_configs, args.duration,
                                           args.headless, args.save_frames, args.output_dir,
                                           args.create_video, args.video_fps)
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
            print("4. Create video from frames")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
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
                
                # Check if we're in a headless environment
                headless = input("Run in headless mode? (y/n, default n): ").strip().lower() == 'y'
                save_frames = False
                output_dir = "frames"
                create_video = False
                video_fps = 10
                
                if headless:
                    save_frames = input("Save frames to files? (y/n, default n): ").strip().lower() == 'y'
                    if save_frames:
                        output_dir = input("Output directory (default 'frames'): ").strip() or "frames"
                        create_video = input("Create video from frames? (y/n, default n): ").strip().lower() == 'y'
                        if create_video:
                            fps_input = input("Video FPS (default 10): ").strip()
                            video_fps = int(fps_input) if fps_input.isdigit() else 10
                
                tester.display_camera_feed(url, name, duration, headless, save_frames, output_dir, create_video, video_fps)
                
            elif choice == "4":
                frames_dir = input("Enter frames directory path: ").strip()
                output_video = input("Enter output video filename (default 'output_video.mp4'): ").strip() or "output_video.mp4"
                fps_input = input("Enter video FPS (default 10): ").strip()
                video_fps = int(fps_input) if fps_input.isdigit() else 10
                
                success = tester.create_video_from_frames(frames_dir, output_video, video_fps)
                print("✅ Video created successfully" if success else "❌ Failed to create video")
                
            elif choice == "5":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 