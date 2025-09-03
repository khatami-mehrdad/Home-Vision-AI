import cv2
import asyncio
import threading
import time
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from app.core.config import settings
from app.models.camera import Camera
from app.services.ai_detection_service import ai_detection_service

logger = logging.getLogger(__name__)

class CameraService:
    def __init__(self):
        self.active_streams: Dict[int, Dict[str, Any]] = {}
        self.stream_locks: Dict[int, threading.Lock] = {}
    
    async def start_camera_stream(self, camera: Camera) -> bool:
        """Start streaming from a camera"""
        if camera.id in self.active_streams:
            logger.info(f"Camera {camera.id} is already streaming")
            return True
        
        try:
            # Create a lock for this camera
            self.stream_locks[camera.id] = threading.Lock()
            
            # Start streaming in a separate thread
            thread = threading.Thread(
                target=self._stream_camera,
                args=(camera,),
                daemon=True
            )
            thread.start()
            
            # Wait a bit to see if stream starts successfully
            await asyncio.sleep(2)
            
            if camera.id in self.active_streams:
                logger.info(f"Successfully started stream for camera {camera.id}")
                return True
            else:
                logger.error(f"Failed to start stream for camera {camera.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting camera stream: {e}")
            return False
    
    def _stream_camera(self, camera: Camera):
        """Internal method to handle DeGirum direct stream processing"""
        try:
            logger.info(f"Starting DeGirum stream processing for: {camera.rtsp_url}")
            
            # Initialize stream data with Smart NVR capabilities
            self.active_streams[camera.id] = {
                "rtsp_url": camera.rtsp_url,
                "last_frame": None,
                "last_frame_time": None,
                "last_detections": [],
                "last_tracks": [],
                "last_events": [],
                "is_running": True,
                "error_count": 0
            }
            
            logger.info(f"Started DeGirum streaming for camera {camera.id}: {camera.name}")
            
            # Process DeGirum stream directly with RTSP URL
            try:
                for nvr_result in ai_detection_service.process_degirum_stream(camera.rtsp_url, camera.id):
                    if not self.active_streams.get(camera.id, {}).get("is_running", False):
                        break
                    
                    # Extract DeGirum results
                    processed_frame = nvr_result["processed_frame"]  # This is inference_result.image_overlay
                    detections = nvr_result["detections"]
                    tracks = nvr_result["tracks"]
                    events = nvr_result["events"]
                    
                    # Store latest frame and Smart NVR data
                    with self.stream_locks[camera.id]:
                        self.active_streams[camera.id]["last_frame"] = processed_frame
                        self.active_streams[camera.id]["last_frame_time"] = datetime.now()
                        self.active_streams[camera.id]["last_detections"] = detections
                        self.active_streams[camera.id]["last_tracks"] = tracks
                        self.active_streams[camera.id]["last_events"] = events
                        self.active_streams[camera.id]["error_count"] = 0
                    
                    logger.debug(f"Processed DeGirum frame for camera {camera.id}, detections: {len(detections)}")
                    
            except Exception as stream_error:
                logger.error(f"Error in DeGirum stream processing for camera {camera.id}: {stream_error}")
                if camera.id in self.active_streams:
                    self.active_streams[camera.id]["error_count"] += 1
                
        except Exception as e:
            logger.error(f"Error setting up DeGirum stream for camera {camera.id}: {e}")
        finally:
            # Clean up stream data
            if camera.id in self.active_streams:
                del self.active_streams[camera.id]
            if camera.id in self.stream_locks:
                del self.stream_locks[camera.id]
    

    
    def get_latest_frame(self, camera_id: int) -> Optional[bytes]:
        """Get the latest frame from DeGirum processing as JPEG bytes"""
        if camera_id not in self.active_streams:
            return None
        
        try:
            with self.stream_locks[camera_id]:
                frame = self.active_streams[camera_id]["last_frame"]  # This is DeGirum's image_overlay
                if frame is not None:
                    # DeGirum frame might already be in the right format
                    # Try to encode as JPEG if it's a numpy array
                    if hasattr(frame, 'shape'):  # numpy array
                        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        if ret:
                            return buffer.tobytes()
                    elif isinstance(frame, bytes):  # already encoded
                        return frame
                    else:
                        logger.warning(f"Unexpected frame type for camera {camera_id}: {type(frame)}")
        except Exception as e:
            logger.error(f"Error getting DeGirum frame from camera {camera_id}: {e}")
        
        return None
    
    def get_camera_status(self, camera_id: int) -> Dict[str, Any]:
        """Get status information for a camera"""
        if camera_id not in self.active_streams:
            return {
                "is_streaming": False,
                "last_frame_time": None,
                "error_count": 0
            }
        
        stream_data = self.active_streams[camera_id]
        return {
            "is_streaming": stream_data["is_running"],
            "last_frame_time": stream_data["last_frame_time"],
            "error_count": stream_data["error_count"]
        }
    
    def get_all_camera_statuses(self) -> Dict[int, Dict[str, Any]]:
        """Get status for all active cameras"""
        return {
            camera_id: self.get_camera_status(camera_id)
            for camera_id in self.active_streams.keys()
        }
    
    def get_latest_detections(self, camera_id: int) -> List[Dict[str, Any]]:
        """Get latest AI detection results from a camera"""
        if camera_id not in self.active_streams:
            return []
        
        try:
            with self.stream_locks[camera_id]:
                detections = self.active_streams[camera_id].get("last_detections", [])
                return detections if detections else []
        except Exception as e:
            logger.error(f"Error getting detections from camera {camera_id}: {e}")
            return []
    
    def get_latest_tracks(self, camera_id: int) -> List[Dict[str, Any]]:
        """Get latest object tracking data from a camera"""
        if camera_id not in self.active_streams:
            return []
        
        try:
            with self.stream_locks[camera_id]:
                tracks = self.active_streams[camera_id].get("last_tracks", [])
                return tracks if tracks else []
        except Exception as e:
            logger.error(f"Error getting tracks from camera {camera_id}: {e}")
            return []
    
    def get_latest_events(self, camera_id: int) -> List[Dict[str, Any]]:
        """Get latest Smart NVR events from a camera"""
        if camera_id not in self.active_streams:
            return []
        
        try:
            with self.stream_locks[camera_id]:
                events = self.active_streams[camera_id].get("last_events", [])
                return events if events else []
        except Exception as e:
            logger.error(f"Error getting events from camera {camera_id}: {e}")
            return []
    
    async def stop_camera_stream(self, camera_id: int) -> bool:
        """Stop DeGirum streaming from a camera and clean up Smart NVR data"""
        if camera_id not in self.active_streams:
            return True
        
        try:
            # Stop the stream processing
            self.active_streams[camera_id]["is_running"] = False
            
            # Clean up Smart NVR data
            ai_detection_service.clear_camera_data(camera_id)
            
            # Remove from active streams
            del self.active_streams[camera_id]
            if camera_id in self.stream_locks:
                del self.stream_locks[camera_id]
            
            logger.info(f"Stopped DeGirum stream for camera {camera_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping DeGirum camera stream {camera_id}: {e}")
            return False

# Global camera service instance
camera_service = CameraService() 