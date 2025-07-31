from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class CameraBase(BaseModel):
    name: str
    rtsp_url: str
    location: Optional[str] = None
    frame_rate: Optional[int] = 10
    resolution: Optional[str] = "1080p"
    detection_enabled: Optional[bool] = True

class CameraCreate(CameraBase):
    pass

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    rtsp_url: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    frame_rate: Optional[int] = None
    resolution: Optional[str] = None
    detection_enabled: Optional[bool] = None

class CameraResponse(CameraBase):
    id: int
    is_active: bool
    is_recording: bool
    status: str
    last_seen: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CameraStatus(BaseModel):
    camera_id: int
    is_streaming: bool
    last_frame_time: Optional[datetime] = None
    error_count: int 