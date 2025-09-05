#!/usr/bin/env python3
"""
Simple camera service that bypasses DeGirum and streams RTSP directly
"""
import cv2
import asyncio
import threading
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as np

logger = logging.getLogger(__name__)

class SimpleCameraService:
    """Simple camera service without AI detection - just direct RTSP streaming"""
    
    def __init__(self):
        self.active_streams: Dict[int, Dict[str, Any]] = {}
        self.stream_locks: Dict[int, threading.Lock] = {}
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="simple_camera_stream")
    
    async def start_camera_stream(self, camera) -> bool:
        """Start simple streaming from a camera without AI detection"""
        logger.info(f"🚀 Starting simple stream for camera {camera.id}: {camera.name}")
        logger.info(f"📹 RTSP URL: {camera.rtsp_url}")
        
        if camera.id in self.active_streams:
            logger.info(f"⚠️ Camera {camera.id} is already streaming")
            return True
        
        try:
            # Test RTSP connection first
            logger.info(f"🔍 Testing RTSP connection...")
            rtsp_test = await self._test_rtsp_connection(camera.rtsp_url)
            if not rtsp_test["success"]:
                logger.error(f"❌ RTSP test failed: {rtsp_test['error']}")
                return False
            
            logger.info(f"✅ RTSP test passed: {rtsp_test['message']}")
            
            # Create lock for this camera
            self.stream_locks[camera.id] = threading.Lock()
            
            # Start streaming in a separate thread
            thread = threading.Thread(
                target=self._simple_stream_camera,
                args=(camera,),
                daemon=True
            )
            thread.start()
            
            # Wait for stream to initialize
            logger.info(f"⏰ Waiting for stream to initialize...")
            for i in range(10):
                await asyncio.sleep(1)
                if camera.id in self.active_streams:
                    logger.info(f"✅ Stream initialized after {i+1} seconds")
                    return True
                logger.info(f"⏳ Still waiting... ({i+1}/10)")
            
            logger.error(f"❌ Failed to start stream after 10 seconds")
            return False
            
        except Exception as e:
            logger.error(f"💥 Exception in start_camera_stream: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def _simple_stream_camera(self, camera):
        """Simple camera streaming without AI detection"""
        camera_id = camera.id
        logger.info(f"🎬 Starting simple camera stream thread for {camera_id}")
        
        try:
            # Initialize stream data
            logger.info(f"🔧 Initializing stream data for camera {camera_id}")
            self.active_streams[camera_id] = {
                "rtsp_url": camera.rtsp_url,
                "last_frame": None,
                "last_frame_time": None,
                "is_running": True,
                "error_count": 0,
                "start_time": datetime.now(),
                "frame_count": 0,
                "fps": 0
            }
            
            # Open RTSP stream
            logger.info(f"📹 Opening RTSP stream: {camera.rtsp_url}")
            cap = cv2.VideoCapture(camera.rtsp_url)
            
            if not cap.isOpened():
                logger.error(f"❌ Failed to open RTSP stream for camera {camera_id}")
                self.active_streams[camera_id]["error_count"] += 1
                return
            
            logger.info(f"✅ RTSP stream opened successfully for camera {camera_id}")
            
            # Get stream properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            logger.info(f"📊 Stream properties: {width}x{height} @ {fps} FPS")
            
            frame_count = 0
            last_fps_time = time.time()
            fps_counter = 0
            
            while self.active_streams.get(camera_id, {}).get("is_running", False):
                ret, frame = cap.read()
                
                if not ret or frame is None:
                    logger.warning(f"⚠️ Failed to read frame from camera {camera_id}")
                    self.active_streams[camera_id]["error_count"] += 1
                    
                    # If too many errors, try to reconnect
                    if self.active_streams[camera_id]["error_count"] > 10:
                        logger.info(f"🔄 Too many errors, attempting to reconnect camera {camera_id}")
                        cap.release()
                        time.sleep(2)  # Wait before reconnecting
                        cap = cv2.VideoCapture(camera.rtsp_url)
                        if not cap.isOpened():
                            logger.error(f"❌ Failed to reconnect to camera {camera_id}")
                            break
                        self.active_streams[camera_id]["error_count"] = 0
                    
                    time.sleep(0.1)
                    continue
                
                # Reset error count on successful frame
                self.active_streams[camera_id]["error_count"] = 0
                frame_count += 1
                fps_counter += 1
                
                # Update stream data
                current_time = datetime.now()
                with self.stream_locks[camera_id]:
                    self.active_streams[camera_id]["last_frame"] = frame
                    self.active_streams[camera_id]["last_frame_time"] = current_time
                    self.active_streams[camera_id]["frame_count"] = frame_count
                
                # Calculate FPS every 30 frames
                if fps_counter >= 30:
                    current_fps_time = time.time()
                    elapsed = current_fps_time - last_fps_time
                    if elapsed > 0:
                        calculated_fps = fps_counter / elapsed
                        self.active_streams[camera_id]["fps"] = round(calculated_fps, 1)
                        logger.debug(f"📈 Camera {camera_id} FPS: {calculated_fps:.1f}")
                    
                    fps_counter = 0
                    last_fps_time = current_fps_time
                
                # Small delay to prevent overwhelming the CPU
                time.sleep(0.033)  # ~30 FPS max
            
            logger.info(f"🛑 Stopping stream for camera {camera_id}")
            cap.release()
            
        except Exception as e:
            logger.error(f"💥 Exception in camera stream thread: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
        finally:
            # Clean up
            if camera_id in self.active_streams:
                del self.active_streams[camera_id]
            if camera_id in self.stream_locks:
                del self.stream_locks[camera_id]
            logger.info(f"🧹 Cleaned up camera {camera_id} stream")
    
    async def stop_camera_stream(self, camera_id: int) -> bool:
        """Stop streaming from a camera"""
        logger.info(f"🛑 Stopping camera {camera_id} stream")
        
        if camera_id not in self.active_streams:
            logger.warning(f"⚠️ Camera {camera_id} is not streaming")
            return True
        
        # Signal the stream to stop
        self.active_streams[camera_id]["is_running"] = False
        
        # Wait a bit for the thread to stop
        await asyncio.sleep(2)
        
        # Force cleanup if still there
        if camera_id in self.active_streams:
            del self.active_streams[camera_id]
        if camera_id in self.stream_locks:
            del self.stream_locks[camera_id]
        
        logger.info(f"✅ Successfully stopped camera {camera_id} stream")
        return True
    
    def get_latest_frame(self, camera_id: int) -> Optional[np.ndarray]:
        """Get the latest frame from a camera"""
        if camera_id not in self.active_streams:
            return None
        
        with self.stream_locks.get(camera_id, threading.Lock()):
            return self.active_streams[camera_id].get("last_frame")
    
    def get_stream_info(self, camera_id: int) -> Dict[str, Any]:
        """Get stream information"""
        if camera_id not in self.active_streams:
            return {"status": "offline", "message": "Stream not active"}
        
        stream_data = self.active_streams[camera_id]
        uptime = datetime.now() - stream_data["start_time"]
        
        return {
            "status": "online",
            "frame_count": stream_data["frame_count"],
            "error_count": stream_data["error_count"],
            "fps": stream_data.get("fps", 0),
            "uptime_seconds": uptime.total_seconds(),
            "last_frame_time": stream_data["last_frame_time"].isoformat() if stream_data["last_frame_time"] else None
        }
    
    async def _test_rtsp_connection(self, rtsp_url: str) -> dict:
        """Test RTSP connection"""
        def test_connection():
            try:
                cap = cv2.VideoCapture(rtsp_url)
                if not cap.isOpened():
                    return {"success": False, "error": "Failed to open RTSP stream"}
                
                ret, frame = cap.read()
                cap.release()
                
                if not ret or frame is None:
                    return {"success": False, "error": "Failed to read frame from RTSP stream"}
                
                return {
                    "success": True, 
                    "frame_shape": frame.shape,
                    "message": "RTSP connection successful"
                }
            except Exception as e:
                return {"success": False, "error": f"RTSP connection error: {str(e)}"}
        
        # Run in thread pool
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(test_connection)
            try:
                result = await asyncio.wrap_future(future)
                return result
            except Exception as e:
                return {"success": False, "error": f"RTSP test exception: {str(e)}"}

# Create global instance
simple_camera_service = SimpleCameraService()
