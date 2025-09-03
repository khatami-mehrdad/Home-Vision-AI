#!/usr/bin/env python3
"""
Test script for DeGirum direct stream processing
Based on DeGirum's object_detection_video_stream example
"""

import sys
import os
# Add the backend directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.ai_detection_service import ai_detection_service
import cv2
import logging

# Enable logging to see debug info
logging.basicConfig(level=logging.INFO)

def test_degirum_stream():
    """Test DeGirum stream processing with RTSP"""
    
    # Your RTSP URL - replace with your camera URL
    rtsp_url = "rtsp://mehrdad:hafez21_M@192.168.1.32:554/stream2"
    camera_id = 1
    
    print("Testing DeGirum Stream Processing...")
    print(f"RTSP URL: {rtsp_url}")
    
    # Check if DeGirum is available
    if ai_detection_service.degirum_model is None:
        print("❌ DeGirum model not available. Please:")
        print("1. Install DeGirum: pip install degirum degirum_tools")
        print("2. Set your token in ai_detection_service.py")
        return
    
    print("✅ DeGirum model loaded successfully")
    
    # Temporarily lower confidence threshold to see more detections
    original_threshold = ai_detection_service.confidence_threshold
    ai_detection_service.confidence_threshold = 0.3  # Lower threshold for testing
    print(f"Lowered confidence threshold to {ai_detection_service.confidence_threshold} for testing")
    
    print("Starting stream processing... Press 'q' to quit")
    
    try:
        frame_count = 0
        for nvr_result in ai_detection_service.process_degirum_stream(rtsp_url, camera_id):
            frame_count += 1
            
            # Get the processed frame with DeGirum overlays
            processed_frame = nvr_result["processed_frame"]  # This is inference_result.image_overlay
            detections = nvr_result["detections"]
            
            print(f"Frame {frame_count}: {len(detections)} detections")
            print(f"  Processed frame type: {type(processed_frame)}")
            print(f"  Processed frame shape: {processed_frame.shape if hasattr(processed_frame, 'shape') else 'N/A'}")
            
            for detection in detections:
                print(f"  - {detection['object_type']}: {detection['confidence']:.2f}")
            
            # Skip display in headless environment - just log frame info
            # if hasattr(processed_frame, 'shape'):  # numpy array
            #     cv2.imshow('DeGirum Stream', processed_frame)
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break
            
            # Limit frames for testing
            if frame_count >= 100:
                print("Reached 100 frames, stopping test")
                break
                
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"❌ Error during stream processing: {e}")
    finally:
        cv2.destroyAllWindows()
        # Restore original confidence threshold
        ai_detection_service.confidence_threshold = original_threshold
    
    print("✅ DeGirum stream test completed")

if __name__ == "__main__":
    test_degirum_stream()
