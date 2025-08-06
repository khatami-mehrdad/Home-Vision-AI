import cv2
import asyncio
import threading
import time
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from app.core.config import settings
from app.models.camera import Camera

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
        """Internal method to handle camera streaming"""
        cap = None
        try:
            logger.info(f"Attempting to open RTSP stream: {camera.rtsp_url}")
            
            # Open RTSP stream
            cap = cv2.VideoCapture(camera.rtsp_url)
            
            if not cap.isOpened():
                logger.error(f"Could not open camera stream: {camera.rtsp_url}")
                return
            
            logger.info(f"Successfully opened camera stream: {camera.rtsp_url}")
            
            # Set camera properties
            cap.set(cv2.CAP_PROP_FPS, camera.frame_rate)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Initialize stream data
            self.active_streams[camera.id] = {
                "cap": cap,
                "last_frame": None,
                "last_frame_time": None,
                "is_running": True,
                "error_count": 0
            }
            
            logger.info(f"Started streaming camera {camera.id}: {camera.name}")
            
            # Stream loop
            while self.active_streams[camera.id]["is_running"]:
                ret, frame = cap.read()
                
                if not ret:
                    self.active_streams[camera.id]["error_count"] += 1
                    logger.warning(f"Failed to read frame from camera {camera.id} (error count: {self.active_streams[camera.id]['error_count']})")
                    
                    if self.active_streams[camera.id]["error_count"] > 10:
                        logger.error(f"Too many errors from camera {camera.id}, stopping stream")
                        break
                    
                    time.sleep(1)
                    continue
                
                # Reset error count on successful frame
                self.active_streams[camera.id]["error_count"] = 0
                
                # Store latest frame
                with self.stream_locks[camera.id]:
                    self.active_streams[camera.id]["last_frame"] = frame
                    self.active_streams[camera.id]["last_frame_time"] = datetime.now()
                
                logger.debug(f"Captured frame from camera {camera.id}: {frame.shape}")
                
                # Control frame rate
                time.sleep(1 / camera.frame_rate)
                
        except Exception as e:
            logger.error(f"Error in camera stream {camera.id}: {e}")
        finally:
            if cap:
                cap.release()
            if camera.id in self.active_streams:
                del self.active_streams[camera.id]
            if camera.id in self.stream_locks:
                del self.stream_locks[camera.id]
    
    async def stop_camera_stream(self, camera_id: int) -> bool:
        """Stop streaming from a camera"""
        if camera_id not in self.active_streams:
            return True
        
        try:
            self.active_streams[camera_id]["is_running"] = False
            cap = self.active_streams[camera_id]["cap"]
            cap.release()
            
            del self.active_streams[camera_id]
            if camera_id in self.stream_locks:
                del self.stream_locks[camera_id]
            
            logger.info(f"Stopped stream for camera {camera_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping camera stream {camera_id}: {e}")
            return False
    
    def get_latest_frame(self, camera_id: int) -> Optional[bytes]:
        """Get the latest frame from a camera as JPEG bytes"""
        if camera_id not in self.active_streams:
            return None
        
        try:
            with self.stream_locks[camera_id]:
                frame = self.active_streams[camera_id]["last_frame"]
                if frame is not None:
                    # Encode frame as JPEG
                    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    if ret:
                        return buffer.tobytes()
        except Exception as e:
            logger.error(f"Error getting frame from camera {camera_id}: {e}")
        
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

# Global camera service instance
camera_service = CameraService() 