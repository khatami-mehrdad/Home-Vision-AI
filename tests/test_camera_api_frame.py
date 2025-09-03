#!/usr/bin/env python3
"""
Test script to verify camera API is serving DeGirum frames with overlays
"""

import requests
import cv2
import numpy as np
from io import BytesIO

def test_camera_api_frame():
    """Test getting camera frame via API"""
    
    camera_id = 1
    api_url = f"http://localhost:8000/api/v1/cameras/{camera_id}/frame"
    
    print(f"Testing camera API frame endpoint: {api_url}")
    
    try:
        # Make request to get camera frame
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully got camera frame from API")
            print(f"  Content-Type: {response.headers.get('content-type')}")
            print(f"  Frame size: {len(response.content)} bytes")
            
            # Try to decode the image
            try:
                # Convert bytes to numpy array
                nparr = np.frombuffer(response.content, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is not None:
                    print(f"✅ Successfully decoded image: {img.shape}")
                    
                    # Save the frame for inspection
                    output_file = f"/home/mehrdad/wa/Home-Vision-AI/tests/degirum_frame_camera_{camera_id}.jpg"
                    cv2.imwrite(output_file, img)
                    print(f"✅ Saved frame to: {output_file}")
                    
                    # Check if frame looks like it has overlays (look for colored pixels that might be bounding boxes)
                    unique_colors = len(np.unique(img.reshape(-1, img.shape[2]), axis=0))
                    print(f"  Frame has {unique_colors} unique colors (more colors = likely has overlays)")
                    
                else:
                    print("❌ Failed to decode image from API response")
                    
            except Exception as decode_error:
                print(f"❌ Error decoding image: {decode_error}")
                
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the backend is running:")
        print("  cd backend && python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error testing camera API: {e}")

def test_camera_status():
    """Test camera status to see if streaming is active"""
    
    camera_id = 1
    api_url = f"http://localhost:8000/api/v1/cameras/{camera_id}/status"
    
    print(f"\nTesting camera status: {api_url}")
    
    try:
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            status = response.json()
            print("✅ Camera status:")
            print(f"  Status: {status.get('status', 'unknown')}")
            print(f"  Is streaming: {status.get('is_streaming', False)}")
            print(f"  Last frame time: {status.get('last_frame_time', 'N/A')}")
            print(f"  Error count: {status.get('error_count', 0)}")
        else:
            print(f"❌ Status request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting camera status: {e}")

if __name__ == "__main__":
    print("🎥 Testing Camera API Frame Endpoint")
    print("=" * 50)
    
    # Test camera status first
    test_camera_status()
    
    print("\n" + "=" * 50)
    
    # Test getting frame
    test_camera_api_frame()
    
    print("\n✅ Camera API test completed!")
    print("\nIf successful, check the saved frame file to see DeGirum overlays!")
