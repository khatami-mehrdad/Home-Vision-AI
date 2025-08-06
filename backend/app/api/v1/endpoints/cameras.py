from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional
import io
import cv2
import numpy as np
import json
import os

from app.models.camera import Camera
from app.services.camera_service import camera_service
from app.schemas.camera import CameraCreate, CameraUpdate, CameraResponse

router = APIRouter()

def load_camera_config():
    """Load camera configuration from JSON file"""
    try:
        # Look for config file relative to project root
        config_paths = [
            "tests/camera_config.json",
            "../tests/camera_config.json",
            "../../tests/camera_config.json"
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    print(f"Loaded camera config from {config_path}: {config}")
                    return config
        
        print("No camera config file found")
        return {}
    except Exception as e:
        print(f"Error loading camera config: {e}")
        return {}

def create_test_frame():
    """Create a test frame for demonstration"""
    # Create a simple test image
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some text and shapes
    cv2.putText(frame, "Test Camera Feed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "Camera ID: 1", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Status: Online", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Add a timestamp
    import time
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Add some visual elements
    cv2.rectangle(frame, (100, 150), (300, 350), (255, 0, 0), 2)
    cv2.circle(frame, (200, 250), 50, (0, 255, 255), -1)
    
    return frame

@router.get("/", response_model=List[CameraResponse])
async def get_cameras():
    """Get all cameras"""
    # Load real camera configuration
    camera_config = load_camera_config()
    
    cameras = []
    for i, (name, rtsp_url) in enumerate(camera_config.items(), 1):
        cameras.append({
            "id": i,
            "name": name,
            "rtsp_url": rtsp_url,
            "location": "Home",
            "is_active": True,
            "is_recording": False,
            "status": "online",
            "frame_rate": 10,
            "resolution": "1080p",
            "detection_enabled": True
        })
    
    # If no real cameras, return mock data
    if not cameras:
        cameras = [{
            "id": 1,
            "name": "Front Door Camera",
            "rtsp_url": "rtsp://192.168.1.100:554/stream1",
            "location": "Front Door",
            "is_active": True,
            "is_recording": False,
            "status": "online",
            "frame_rate": 10,
            "resolution": "1080p",
            "detection_enabled": True
        }]
    
    return cameras

@router.post("/", response_model=CameraResponse)
async def create_camera(camera: CameraCreate):
    """Create a new camera"""
    # This would typically save to database
    return {
        "id": 1,
        "name": camera.name,
        "rtsp_url": camera.rtsp_url,
        "location": camera.location,
        "is_active": True,
        "is_recording": False,
        "status": "offline",
        "frame_rate": camera.frame_rate,
        "resolution": camera.resolution,
        "detection_enabled": camera.detection_enabled
    }

@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: int):
    """Get a specific camera"""
    # Load real camera configuration
    camera_config = load_camera_config()
    camera_names = list(camera_config.keys())
    
    if camera_id <= len(camera_names):
        camera_name = camera_names[camera_id - 1]
        rtsp_url = camera_config[camera_name]
        return {
            "id": camera_id,
            "name": camera_name,
            "rtsp_url": rtsp_url,
            "location": "Home",
            "is_active": True,
            "is_recording": False,
            "status": "online",
            "frame_rate": 10,
            "resolution": "1080p",
            "detection_enabled": True
        }
    else:
        # Return mock data for non-existent cameras
        return {
            "id": camera_id,
            "name": "Front Door Camera",
            "rtsp_url": "rtsp://192.168.1.100:554/stream1",
            "location": "Front Door",
            "is_active": True,
            "is_recording": False,
            "status": "online",
            "frame_rate": 10,
            "resolution": "1080p",
            "detection_enabled": True
        }

@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(camera_id: int, camera_update: CameraUpdate):
    """Update a camera"""
    # This would typically update in database
    return {
        "id": camera_id,
        "name": camera_update.name or "Updated Camera",
        "rtsp_url": camera_update.rtsp_url or "rtsp://192.168.1.100:554/stream1",
        "location": camera_update.location or "Updated Location",
        "is_active": camera_update.is_active if camera_update.is_active is not None else True,
        "is_recording": False,
        "status": "online",
        "frame_rate": camera_update.frame_rate or 10,
        "resolution": camera_update.resolution or "1080p",
        "detection_enabled": camera_update.detection_enabled if camera_update.detection_enabled is not None else True
    }

@router.delete("/{camera_id}")
async def delete_camera(camera_id: int):
    """Delete a camera"""
    # Stop streaming if active
    await camera_service.stop_camera_stream(camera_id)
    return {"message": f"Camera {camera_id} deleted successfully"}

@router.post("/{camera_id}/start")
async def start_camera_stream(camera_id: int):
    """Start streaming from a camera"""
    # Load real camera configuration
    camera_config = load_camera_config()
    camera_names = list(camera_config.keys())
    
    if camera_id <= len(camera_names):
        camera_name = camera_names[camera_id - 1]
        rtsp_url = camera_config[camera_name]
        
        # Create camera object with real RTSP URL
        camera = Camera(
            id=camera_id,
            name=camera_name,
            rtsp_url=rtsp_url,
            frame_rate=10
        )
        
        # Try to start the real camera stream
        success = await camera_service.start_camera_stream(camera)
        if success:
            return {"message": f"Camera {camera_id} ({camera_name}) stream started successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to start camera stream")
    else:
        # For demo purposes, simulate success
        return {"message": f"Camera {camera_id} stream started successfully (demo mode)"}

@router.post("/{camera_id}/stop")
async def stop_camera_stream(camera_id: int):
    """Stop streaming from a camera"""
    success = await camera_service.stop_camera_stream(camera_id)
    if success:
        return {"message": f"Camera {camera_id} stream stopped successfully"}
    else:
        # For demo purposes, always return success
        return {"message": f"Camera {camera_id} stream stopped successfully"}

@router.get("/{camera_id}/frame")
async def get_camera_frame(camera_id: int):
    """Get the latest frame from a camera"""
    # Try to get real frame from camera service
    frame_bytes = camera_service.get_latest_frame(camera_id)
    
    if frame_bytes is None:
        # Return a test frame if no real frame is available
        test_frame = create_test_frame()
        ret, buffer = cv2.imencode('.jpg', test_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if ret:
            frame_bytes = buffer.tobytes()
        else:
            raise HTTPException(status_code=404, detail="Failed to create test frame")
    
    return StreamingResponse(
        io.BytesIO(frame_bytes),
        media_type="image/jpeg",
        headers={"Cache-Control": "no-cache"}
    )

@router.get("/{camera_id}/status")
async def get_camera_status(camera_id: int):
    """Get status information for a camera"""
    status = camera_service.get_camera_status(camera_id)
    return {
        "camera_id": camera_id,
        **status
    }

@router.get("/status/all")
async def get_all_camera_statuses():
    """Get status for all active cameras"""
    return camera_service.get_all_camera_statuses() 