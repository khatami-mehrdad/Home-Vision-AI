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
                "labelmap_path": "/labelmap.txt"
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
                    "stream_name": camera_name.lower().replace(" ", "_"),
                    "height": 720,
                    "quality": 8
                },
                "ui": {
                    "order": idx,
                    "dashboard": True
                },
                "name": camera_stream_name
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
        for camera in cameras:
            camera_name = camera.get("name", "unknown")
            # Mock camera being online and processing
            stats["cameras"][camera_name] = {
                "camera_fps": 5.0,
                "capture_pid": 1234,
                "detection_fps": 2.5,
                "pid": 1234,
                "process_fps": 5.0,
                "skipped_fps": 0.0,
                "detection_enabled": True,
                "detection_frame": current_time
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
    Get latest camera image (WebP format) with AI detection overlays
    This is the main endpoint that Frigate UI uses for camera images
    """
    from fastapi.responses import Response
    import io
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import time
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Create a test frame that simulates a camera feed
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add some test content to make it look like a real camera feed
        cv2.rectangle(frame, (50, 50), (590, 430), (100, 100, 100), 2)
        cv2.putText(frame, f"Camera: {camera}", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Resolution: {height}px", (60, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, f"Time: {time.strftime('%H:%M:%S')}", (60, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Try to use DeGirum AI detection if available
        try:
            from app.services.ai_detection_service import ai_detection_service
            
            # Check if DeGirum is available and properly initialized
            if (hasattr(ai_detection_service, 'degirum_model') and 
                ai_detection_service.degirum_model is not None and
                hasattr(ai_detection_service, 'is_initialized') and 
                ai_detection_service.is_initialized):
                
                # Use DeGirum for AI detection
                detection_result = ai_detection_service.process_frame(frame, camera_id=1)
                
                if detection_result and "processed_frame" in detection_result:
                    processed_frame = detection_result["processed_frame"]
                    detections = detection_result.get("detections", [])
                    
                    # Add AI status indicator
                    cv2.putText(processed_frame, "AI Detection: ACTIVE", (60, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(processed_frame, f"Objects: {len(detections)}", (60, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                    
                    # Convert BGR to RGB for PIL
                    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                else:
                    raise Exception("DeGirum processing failed")
            else:
                raise Exception("DeGirum model not available or not initialized")
                
        except Exception as e:
            logger.warning(f"DeGirum AI detection not available: {e}")
            
            # Fallback: Create mock detections for demo
            import random
            
            # Create dynamic detections that change over time
            current_time = int(time.time())
            random.seed(current_time // 5)  # Change every 5 seconds
            
            # Randomly generate 0-3 detections
            num_detections = random.randint(0, 3)
            mock_detections = []
            
            object_types = ["person", "car", "bicycle", "dog", "cat", "truck", "motorcycle"]
            
            for i in range(num_detections):
                obj_type = random.choice(object_types)
                confidence = random.uniform(0.7, 0.95)
                
                # Random bounding box position
                x = random.randint(100, 500)
                y = random.randint(150, 350)
                w = random.randint(60, 150)
                h = random.randint(60, 200)
                
                mock_detections.append({
                    "object_type": obj_type,
                    "confidence": confidence,
                    "bounding_box": [x, y, w, h],
                    "center": [x + w//2, y + h//2]
                })
            
            # Draw mock detections
            for detection in mock_detections:
                bbox = detection["bounding_box"]
                x, y, w, h = bbox
                confidence = detection["confidence"]
                obj_type = detection["object_type"]
                
                # Color code by object type
                color_map = {
                    "person": (0, 255, 0),      # Green
                    "car": (255, 0, 0),         # Blue
                    "truck": (255, 0, 0),       # Blue
                    "motorcycle": (255, 0, 0),  # Blue
                    "bicycle": (0, 255, 255),   # Yellow
                    "dog": (255, 0, 255),       # Magenta
                    "cat": (255, 0, 255),       # Magenta
                }
                
                # Get color for object type, default to white
                color = color_map.get(obj_type, (255, 255, 255))
                
                # Make color darker for low confidence
                if confidence < 0.8:
                    color = tuple(int(c * 0.7) for c in color)
                
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                
                # Draw label with background
                label = f"{obj_type}: {confidence:.2f}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(frame, (x, y - label_size[1] - 10), (x + label_size[0], y), color, -1)
                cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Add AI status indicator
            cv2.putText(frame, "AI Detection: DEMO MODE", (60, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Objects: {len(mock_detections)}", (60, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Convert BGR to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(frame_rgb)
        
        # Resize if needed
        if height != 480:
            pil_image = pil_image.resize((int(640 * height / 480), height), Image.Resampling.LANCZOS)
        
        # Convert to WebP
        webp_buffer = io.BytesIO()
        pil_image.save(webp_buffer, format='WEBP', quality=85)
        webp_data = webp_buffer.getvalue()
        
        # Count detections for logging
        detection_count = 0
        if 'detections' in locals():
            detection_count = len(detections)
        elif 'mock_detections' in locals():
            detection_count = len(mock_detections)
        
        logger.info(f"Served AI-processed camera image for {camera} with {detection_count} detections")
        return Response(content=webp_data, media_type="image/webp")
        
    except Exception as e:
        logger.error(f"Error generating camera image for {camera}: {e}")
        
        # Fallback to placeholder image
        img = Image.new('RGB', (640, 480), color='black')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"Camera: {camera}\nHeight: {height}px\nAI Detection: ERROR\nTime: {time.strftime('%H:%M:%S')}"
        draw.multiline_text((50, 200), text, fill='red', font=font, align='center')
        
        webp_buffer = io.BytesIO()
        img.save(webp_buffer, format='WEBP', quality=80)
        webp_data = webp_buffer.getvalue()
        
        return Response(content=webp_data, media_type="image/webp")
