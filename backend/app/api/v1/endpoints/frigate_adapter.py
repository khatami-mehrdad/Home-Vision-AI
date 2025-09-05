"""
Frigate API Adapter Endpoints
Provides Frigate-compatible API endpoints for the Home Vision AI backend
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
import logging

from app.services.camera_service import camera_service
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()

def load_camera_config():
    """Load camera configuration from JSON file"""
    try:
        config_paths = [
            "camera_config.json",
            "../camera_config.json", 
            "../../camera_config.json"
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        return {"cameras": []}
    except Exception as e:
        logger.error(f"Error loading camera config: {e}")
        return {"cameras": []}

@router.get("/config")
async def get_frigate_config():
    """
    Get Frigate-compatible configuration
    Adapts Home Vision AI camera configuration to Frigate format
    """
    try:
        # Load camera configuration
        config_data = load_camera_config()
        cameras = config_data.get("cameras", [])
        
        # Create Frigate-compatible config
        frigate_config = {
            "cameras": {},
            "camera_groups": {},
            "mqtt": {
                "enabled": False
            },
            "detect": {
                "enabled": True,
                "width": 1280,
                "height": 720,
                "fps": 5
            },
            "record": {
                "enabled": True,
                "retain": {
                    "days": 7,
                    "mode": "motion"
                }
            },
            "snapshots": {
                "enabled": True,
                "timestamp": True,
                "bounding_box": True,
                "crop": False,
                "height": 270
            },
            "objects": {
                "track": ["person", "cat", "car"],
                "filters": {
                    "person": {
                        "min_area": 5000,
                        "max_area": 100000,
                        "threshold": 0.7
                    },
                    "cat": {
                        "min_area": 1000,
                        "max_area": 50000,
                        "threshold": 0.7
                    },
                    "car": {
                        "min_area": 10000,
                        "max_area": 200000,
                        "threshold": 0.7
                    }
                }
            },
            "go2rtc": {
                "streams": {}
            },
            "ffmpeg": {
                "global_args": ["-hide_banner", "-loglevel", "warning"],
                "hwaccel_args": "preset-vaapi",
                "input_args": "preset-rtsp-restream",
                "output_args": {
                    "detect": "-threads 2 -f rawvideo -pix_fmt yuv420p",
                    "record": "preset-record-generic-audio-aac",
                    "rtmp": "preset-rtmp-generic"
                }
            },
            "ui": {
                "live_mode": "mse",
                "timezone": "America/New_York",
                "use_experimental": False
            },
            "frigate": {
                "full_system": True,
                "system_stats": True,
                "gpu_stats": True,
                "process_info": True
            },
            "model": {
                "width": 320,
                "height": 320,
                "input_tensor": "normalized_input_image_tensor",
                "input_pixel_format": "rgb",
                "path": "/cpu_model.tflite",
                "labelmap_path": "/labelmap.txt",
                "attributes_map": {}  # Required by frontend iconUtil
            },
            "detectors": {
                "cpu": {
                    "type": "cpu",
                    "num_threads": 3
                }
            },
            "logger": {
                "default": "info",
                "logs": {
                    "frigate.app": "info",
                    "frigate.mqtt": "info"
                }
            },
            "database": {
                "path": "/db/frigate.db"
            },
            "version": "0.14.0",
            "service_version": "1.0.0",
            "safe_mode": False
        }
        
        # Convert each camera to Frigate format
        for idx, camera in enumerate(cameras):
            camera_name = camera.get("name", f"camera_{idx}")
            camera_stream_name = camera.get("stream_name", camera_name.lower().replace(" ", "_"))
            rtsp_url = camera.get("rtsp_url", "")
            
            frigate_config["cameras"][camera_stream_name] = {
                "enabled": True,
                "enabled_in_config": True,  # Required by Live tab frontend
                "ffmpeg": {
                    "inputs": [
                        {
                            "path": rtsp_url,
                            "roles": ["detect", "record"]
                        }
                    ]
                },
                "detect": {
                    "enabled": True,
                    "width": 1280,
                    "height": 720,
                    "fps": 5
                },
                "record": {
                    "enabled": True,
                    "enabled_in_config": True,  # Required by LiveCameraView
                    "retain": {
                        "days": 7,
                        "mode": "motion"
                    }
                },
                "snapshots": {
                    "enabled": True,
                    "timestamp": True,
                    "bounding_box": True,
                    "crop": False,
                    "height": 270
                },
                "objects": {
                    "track": ["person", "cat", "car"],
                    "filters": {}
                },
                "zones": {},
                "live": {
                    "stream_name": camera_stream_name,
                    "height": 720,
                    "quality": 8,
                    "streams": {
                        camera_stream_name: camera_stream_name
                    }
                },
                "ui": {
                    "order": idx,
                    "dashboard": True
                },
                "name": camera_stream_name,
                "audio": {
                    "enabled": False,
                    "enabled_in_config": False  # Required by LiveCameraView
                },
                "onvif": {
                    "autotracking": {
                        "enabled": False,
                        "enabled_in_config": False  # Required by LiveCameraView
                    }
                },
                "audio_transcription": {
                    "enabled": False,
                    "enabled_in_config": False  # Required by LiveCameraView
                }
            }
            
            # Add to go2rtc streams
            frigate_config["go2rtc"]["streams"][camera_name.lower().replace(" ", "_")] = rtsp_url
        
        return frigate_config
        
    except Exception as e:
        logger.error(f"Error generating Frigate config: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating configuration: {str(e)}")

@router.get("/stats")
async def get_frigate_stats():
    """
    Get Frigate-compatible system statistics
    """
    try:
        # Load camera configuration to get camera names
        config_data = load_camera_config()
        cameras = config_data.get("cameras", [])
        
        # Get current timestamp
        current_time = datetime.now().timestamp()
        
        # Create mock stats in Frigate format
        stats = {
            "service": {
                "uptime": current_time - 3600,  # 1 hour uptime
                "version": "1.0.0",
                "latest_version": "1.0.0",
                "storage": {
                    "/media/frigate/clips": {
                        "total": 1000000000,  # 1GB
                        "used": 500000000,    # 500MB  
                        "free": 500000000     # 500MB
                    }
                }
            },
            "cameras": {},
            "detectors": {
                "cpu": {
                    "detection_start": 0,
                    "inference_speed": 100.0,
                    "pid": 1234
                }
                    },
        "cpu_usages": {
            "frigate.full_system": {
                "cpu": "15.2",
                "cpu_average": "12.8",
                "mem": "2.1"
            }
        },
        "gpu_usages": {},
        "processes": {}
        }
        
        # Add camera stats
        for idx, camera in enumerate(cameras):
            camera_name = camera.get("name", f"camera_{idx}")
            camera_stream_name = camera_name.lower().replace(" ", "_")
            
            # Mock camera being online and processing
            stats["cameras"][camera_stream_name] = {
                "camera_fps": 5.0,
                "capture_pid": 1234,
                "detection_fps": 2.5,
                "pid": 1234,
                "process_fps": 5.0,
                "skipped_fps": 0.0,
                "detection_enabled": True,
                "detection_frame": current_time,
                "enabled": True  # Add the enabled field that the frontend expects
            }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error generating Frigate stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating stats: {str(e)}")

@router.get("/events")
async def get_frigate_events(
    limit: int = 25,
    camera: Optional[str] = None,
    label: Optional[str] = None,
    zone: Optional[str] = None,
    after: Optional[float] = None,
    before: Optional[float] = None
):
    """
    Get Frigate-compatible events
    For now returns empty array - you'll need to implement event storage
    """
    try:
        # TODO: Implement event storage and retrieval in your backend
        # This would query your database for detection events
        
        # Return empty events for now
        events = []
        
        return events
        
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")

@router.get("/recordings/{camera}")
async def get_camera_recordings(camera: str, date: str):
    """
    Get recordings for a specific camera and date
    """
    try:
        # TODO: Implement recording storage and retrieval
        # This would return available recordings for the camera/date
        
        return []
        
    except Exception as e:
        logger.error(f"Error fetching recordings: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching recordings: {str(e)}")

@router.get("/version")
async def get_version():
    """Get version information"""
    return {
        "version": "1.0.0",
        "latest_version": "1.0.0"
    }

@router.get("/profile")
async def get_profile():
    """Get user profile information"""
    return {
        "username": "admin",
        "roles": ["admin"],
        "preferences": {}
    }

@router.get("/logs/{service}")
async def get_logs(service: str, lines: int = 100):
    """Get service logs"""
    return []

@router.get("/restart")
async def restart_service():
    """Restart service endpoint"""
    return {"message": "Service restart requested"}

@router.get("/review")
async def get_review(
    limit: int = 10,
    severity: str = "alert"
):
    """
    Get review/events data (mock implementation for now)
    This endpoint provides events/alerts that show in the Frigate UI
    """
    return []

@router.get("/live/current/{camera}")
async def get_camera_current_image(camera: str):
    """
    Get current camera image (snapshot)
    This is what Frigate UI uses when live stream is not available
    """
    # For now, return a placeholder response
    # In a real implementation, this would return the latest camera frame
    return {"message": f"Current image for {camera} not available"}

@router.get("/{camera}/latest.jpg")
async def get_camera_latest_jpg(camera: str):
    """Get latest camera image (JPEG format)"""
    from fastapi.responses import Response
    return Response(content=b"", media_type="image/jpeg")

@router.get("/{camera}/latest.webp")
async def get_camera_latest_webp(camera: str, height: int = 360):
    """
    Get latest camera image (WebP format) directly from RTSP stream
    This is the main endpoint that Frigate UI uses for camera images
    """
    from fastapi.responses import Response
    import io
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import time
    import logging
    import json
    import os
    
    logger = logging.getLogger(__name__)
    
    try:
        # Load camera configuration
        config_path = "/home/mehrdad/wa/Home-Vision-AI/camera_config.json"
        if not os.path.exists(config_path):
            raise Exception(f"Camera config not found at {config_path}")
        
        with open(config_path, 'r') as f:
            camera_config = json.load(f)
        
        # Find the camera configuration
        camera_info = None
        for cam in camera_config.get("cameras", []):
            if cam.get("name", "").lower().replace(" ", "_") == camera:
                camera_info = cam
                break
        
        if not camera_info:
            raise Exception(f"Camera {camera} not found in configuration")
        
        rtsp_url = camera_info.get("rtsp_url")
        if not rtsp_url:
            raise Exception(f"No RTSP URL configured for camera {camera}")
        
        logger.info(f"Connecting to RTSP stream for camera {camera}: {rtsp_url}")
        
        # Connect to RTSP stream
        cap = cv2.VideoCapture(rtsp_url)
        
        if not cap.isOpened():
            raise Exception(f"Failed to open RTSP stream: {rtsp_url}")
        
        # Set buffer size to reduce latency
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Read a frame
        ret, frame = cap.read()
        cap.release()
        
        if not ret or frame is None:
            raise Exception("Failed to read frame from RTSP stream")
        
        logger.info(f"Successfully captured frame from RTSP stream: {frame.shape}")
        
        # Add timestamp overlay
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Camera: {camera}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "RTSP Stream: ACTIVE", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Convert BGR to RGB for PIL
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(frame_rgb)
        
        # Resize if needed
        if height != frame.shape[0]:
            # Calculate new width maintaining aspect ratio
            aspect_ratio = frame.shape[1] / frame.shape[0]
            new_width = int(height * aspect_ratio)
            pil_image = pil_image.resize((new_width, height), Image.Resampling.LANCZOS)
        
        # Convert to WebP
        webp_buffer = io.BytesIO()
        pil_image.save(webp_buffer, format='WEBP', quality=85)
        webp_data = webp_buffer.getvalue()
        
        logger.info(f"Served RTSP camera image for {camera}, WebP size: {len(webp_data)} bytes")
        return Response(content=webp_data, media_type="image/webp")
        
    except Exception as e:
        logger.error(f"Error capturing camera image for {camera}: {e}")
        
        # Fallback to placeholder image
        img = Image.new('RGB', (640, 480), color='black')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        # Add error message
        error_text = f"RTSP Error: {str(e)[:50]}..."
        if font:
            draw.text((20, 20), error_text, fill='white', font=font)
        else:
            draw.text((20, 20), error_text, fill='white')
        
        # Add timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if font:
            draw.text((20, 50), timestamp, fill='gray', font=font)
        else:
            draw.text((20, 50), timestamp, fill='gray')
        
        # Convert to WebP
        webp_buffer = io.BytesIO()
        img.save(webp_buffer, format='WEBP', quality=85)
        webp_data = webp_buffer.getvalue()
        
        return Response(content=webp_data, media_type="image/webp")
