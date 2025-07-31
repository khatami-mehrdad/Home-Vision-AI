from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional
import io

from app.models.camera import Camera
from app.services.camera_service import camera_service
from app.schemas.camera import CameraCreate, CameraUpdate, CameraResponse

router = APIRouter()

@router.get("/", response_model=List[CameraResponse])
async def get_cameras():
    """Get all cameras"""
    # This would typically fetch from database
    # For now, return mock data
    return [
        {
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
        }
    ]

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
    # This would typically fetch from database
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
    # Create mock camera object
    camera = Camera(
        id=camera_id,
        name="Test Camera",
        rtsp_url="rtsp://192.168.1.100:554/stream1",
        frame_rate=10
    )
    
    success = await camera_service.start_camera_stream(camera)
    if success:
        return {"message": f"Camera {camera_id} stream started successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to start camera stream")

@router.post("/{camera_id}/stop")
async def stop_camera_stream(camera_id: int):
    """Stop streaming from a camera"""
    success = await camera_service.stop_camera_stream(camera_id)
    if success:
        return {"message": f"Camera {camera_id} stream stopped successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to stop camera stream")

@router.get("/{camera_id}/frame")
async def get_camera_frame(camera_id: int):
    """Get the latest frame from a camera"""
    frame_bytes = camera_service.get_latest_frame(camera_id)
    
    if frame_bytes is None:
        raise HTTPException(status_code=404, detail="No frame available")
    
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