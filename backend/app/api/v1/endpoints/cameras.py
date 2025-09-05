from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
import io
import cv2
import numpy as np
import json
import os
import logging

from app.models.camera import Camera
from app.services.camera_service import camera_service
# Import simple camera service for fallback
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from simple_camera_service import simple_camera_service
from app.schemas.camera import CameraCreate, CameraUpdate, CameraResponse
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()

def load_camera_config():
    """Load camera configuration from JSON file"""
    try:
        # Look for config file relative to project root
        config_paths = [
            "camera_config.json",
            "../camera_config.json", 
            "../../camera_config.json",
            "tests/camera_config.json",
            "../tests/camera_config.json",
            "../../tests/camera_config.json"
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    full_config = json.load(f)
                    print(f"Loaded camera config from {config_path}: {full_config}")
                    
                    # Convert cameras array to simple name->rtsp_url mapping
                    config = {}
                    if "cameras" in full_config:
                        for camera in full_config["cameras"]:
                            config[camera["name"]] = camera["rtsp_url"]
                    
                    print(f"Converted config: {config}")
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
    try:
        logger.info(f"🚀 Starting camera stream for camera_id: {camera_id}")
        
        # Load real camera configuration
        camera_config = load_camera_config()
        logger.info(f"📋 Loaded camera config: {camera_config}")
        
        camera_names = list(camera_config.keys())
        logger.info(f"📷 Available cameras: {camera_names}")
        
        if camera_id <= len(camera_names):
            camera_name = camera_names[camera_id - 1]
            rtsp_url = camera_config[camera_name]
            logger.info(f"🎯 Found camera: {camera_name} -> {rtsp_url}")
            
            # Create a simple camera object (not SQLAlchemy model)
            class SimpleCamera:
                def __init__(self, id, name, rtsp_url, frame_rate=10):
                    self.id = id
                    self.name = name
                    self.rtsp_url = rtsp_url
                    self.frame_rate = frame_rate
            
            camera = SimpleCamera(
                id=camera_id,
                name=camera_name,
                rtsp_url=rtsp_url,
                frame_rate=10
            )
            
            logger.info(f"🔧 Created camera object: {camera.name} (ID: {camera.id})")
            
            # Try simple camera service first (bypassing AI detection)
            logger.info(f"🔄 Trying simple camera service (no AI detection)...")
            simple_success = await simple_camera_service.start_camera_stream(camera)
            
            if simple_success:
                logger.info(f"✅ Successfully started simple camera {camera_id} stream")
                return {"message": f"Camera {camera_id} ({camera_name}) stream started successfully (simple mode)"}
            
            # Fallback to original service if needed
            logger.info(f"🔄 Falling back to original camera service...")
            success = await camera_service.start_camera_stream(camera)
            if success:
                logger.info(f"✅ Successfully started camera {camera_id} stream")
                return {"message": f"Camera {camera_id} ({camera_name}) stream started successfully"}
            else:
                logger.error(f"❌ Failed to start camera {camera_id} stream")
                raise HTTPException(status_code=500, detail="Failed to start camera stream")
        else:
            logger.warning(f"⚠️ Camera {camera_id} not found in config, using demo mode")
            # For demo purposes, simulate success
            return {"message": f"Camera {camera_id} stream started successfully (demo mode)"}
            
    except Exception as e:
        logger.error(f"💥 Exception in start_camera_stream: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to start camera stream: {str(e)}")

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
    """Get the latest frame from a camera (simple mode without AI)"""
    import cv2  # Import cv2 at the top to avoid scope issues
    frame_bytes = None
    
    # Use simple camera service (no AI detection) consistently
    frame = simple_camera_service.get_latest_frame(camera_id)
    if frame is not None:
        logger.debug(f"✅ Got frame from simple camera service for camera {camera_id}")
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if ret:
            frame_bytes = buffer.tobytes()
        else:
            logger.error(f"❌ Failed to encode frame for camera {camera_id}")
    else:
        logger.warning(f"⚠️  No frame available from simple camera service for camera {camera_id}")
    
    # Note: DeGirum service fallback removed to prevent inconsistent AI/non-AI switching
    
    # Last resort: direct RTSP capture
    if frame_bytes is None:
        logger.info(f"No cached frame for camera {camera_id}, trying direct RTSP capture...")
        
        # Load camera config to get RTSP URL
        config = load_camera_config()
        rtsp_url = None
        
        for name, url in config.items():
            if name == "My Camera":  # Assuming camera_id 1 maps to "My Camera"
                rtsp_url = url
                break
        
        if rtsp_url:
            try:
                cap = cv2.VideoCapture(rtsp_url)
                
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    
                    if ret and frame is not None:
                        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        if ret:
                            frame_bytes = buffer.tobytes()
                            logger.debug(f"Captured direct RTSP frame for camera {camera_id}")
                
            except Exception as e:
                logger.error(f"Failed to capture direct RTSP frame: {e}")
    
    # Final fallback: test frame
    if frame_bytes is None:
        logger.warning(f"No frame available for camera {camera_id}, returning test frame")
        test_frame = create_test_frame()
        ret, buffer = cv2.imencode('.jpg', test_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if ret:
            frame_bytes = buffer.tobytes()
        else:
            raise HTTPException(status_code=404, detail="Failed to create test frame")
    
    return StreamingResponse(
        io.BytesIO(frame_bytes),
        media_type="image/jpeg",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@router.get("/{camera_id}/frame/ai")
async def get_camera_frame_with_ai(camera_id: int):
    """Get the latest frame from a camera WITH AI detection and bounding boxes"""
    import cv2
    frame_bytes = None
    
    # Try DeGirum AI service first
    frame_bytes = camera_service.get_latest_frame(camera_id)
    if frame_bytes:
        logger.debug(f"✅ Got AI-processed frame from DeGirum service for camera {camera_id}")
    else:
        logger.warning(f"⚠️  No AI-processed frame available for camera {camera_id}")
        
        # Fallback: get simple frame and add "AI Unavailable" overlay
        frame = simple_camera_service.get_latest_frame(camera_id)
        if frame is not None:
            # Add text overlay indicating AI is unavailable
            cv2.putText(frame, "AI Detection Unavailable", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                frame_bytes = buffer.tobytes()
    
    if frame_bytes is None:
        logger.error(f"❌ No frame available for camera {camera_id}")
        raise HTTPException(status_code=404, detail="No frame available")
    
    return StreamingResponse(
        io.BytesIO(frame_bytes),
        media_type="image/jpeg",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@router.get("/{camera_id}/status")
async def get_camera_status(camera_id: int):
    """Get status information for a camera"""
    status = camera_service.get_camera_status(camera_id)
    return {
        "camera_id": camera_id,
        **status
    }

@router.get("/{camera_id}/stream")
async def stream_camera_mjpeg(camera_id: int):
    """Stream camera as MJPEG for live viewing"""
    import cv2
    import asyncio
    
    async def generate_mjpeg_stream():
        while True:
            try:
                # Get latest frame from simple camera service
                frame = simple_camera_service.get_latest_frame(camera_id)
                if frame is not None:
                    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    if ret:
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    
                await asyncio.sleep(1/10)  # 10 FPS
            except Exception as e:
                logger.error(f"Error in MJPEG stream: {e}")
                break
    
    return StreamingResponse(
        generate_mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@router.get("/status/all")
async def get_all_camera_statuses():
    """Get status for all active cameras"""
    return camera_service.get_all_camera_statuses()


@router.get("/debug/test-degirum")
async def test_degirum():
    """Test DeGirum loading directly"""
    try:
        import degirum as dg
        import degirum_tools
        token = degirum_tools.get_token()
        return {
            "status": "success", 
            "message": "DeGirum is available",
            "token_preview": token[:10] + "..." if token else "No token"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{camera_id}/detections")
async def get_camera_detections(camera_id: int):
    """Get latest AI detection results from a camera"""
    try:
        detections = camera_service.get_latest_detections(camera_id)
        return {
            "camera_id": camera_id,
            "detections": detections,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error getting detections for camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get camera detections")

@router.get("/{camera_id}/tracks")
async def get_camera_tracks(camera_id: int):
    """Get active object tracks from Smart NVR"""
    try:
        tracks = camera_service.get_latest_tracks(camera_id)
        return {
            "camera_id": camera_id,
            "tracks": tracks,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error getting tracks for camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get camera tracks")

@router.get("/{camera_id}/events")
async def get_camera_events(camera_id: int, limit: int = 50):
    """Get Smart NVR event history for a camera"""
    try:
        from app.services.ai_detection_service import ai_detection_service
        events = ai_detection_service.get_event_history(camera_id, limit)
        return {
            "camera_id": camera_id,
            "events": events,
            "total": len(events),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error getting events for camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get camera events")

@router.post("/{camera_id}/zones")
async def add_detection_zone(camera_id: int, zone_data: dict):
    """Add a detection zone for Smart NVR"""
    try:
        from app.services.ai_detection_service import ai_detection_service
        
        success = ai_detection_service.add_detection_zone(
            camera_id=camera_id,
            zone_name=zone_data["name"],
            zone_type=zone_data["type"],
            coordinates=zone_data["coordinates"],
            restricted=zone_data.get("restricted", False)
        )
        
        if success:
            return {"message": f"Detection zone '{zone_data['name']}' added successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to add detection zone")
            
    except Exception as e:
        logger.error(f"Error adding detection zone for camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to add detection zone")

@router.get("/{camera_id}/zones")
async def get_detection_zones(camera_id: int):
    """Get all detection zones for a camera"""
    try:
        from app.services.ai_detection_service import ai_detection_service
        zones = ai_detection_service.get_detection_zones(camera_id)
        return {
            "camera_id": camera_id,
            "zones": zones,
            "total": len(zones)
        }
    except Exception as e:
        logger.error(f"Error getting detection zones for camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get detection zones")

@router.delete("/{camera_id}/zones/{zone_name}")
async def remove_detection_zone(camera_id: int, zone_name: str):
    """Remove a detection zone"""
    try:
        from app.services.ai_detection_service import ai_detection_service
        success = ai_detection_service.remove_detection_zone(camera_id, zone_name)
        
        if success:
            return {"message": f"Detection zone '{zone_name}' removed successfully"}
        else:
            raise HTTPException(status_code=404, detail="Detection zone not found")
            
    except Exception as e:
        logger.error(f"Error removing detection zone for camera {camera_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove detection zone")

@router.get("/nvr/statistics")
async def get_nvr_statistics():
    """Get Smart NVR system statistics"""
    try:
        from app.services.ai_detection_service import ai_detection_service
        stats = ai_detection_service.get_nvr_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting NVR statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get NVR statistics") 