import json
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class CameraConfigService:
    """Service to manage camera configurations from JSON file"""
    
    def __init__(self):
        self.config_file = self._find_config_file()
        self.config_data = None
        self.load_config()
    
    def _find_config_file(self) -> str:
        """Find the camera config file in various locations"""
        possible_paths = [
            "camera_config.json",
            "../camera_config.json", 
            "../../camera_config.json",
            "/home/mehrdad/wa/Home-Vision-AI/camera_config.json",
            "tests/camera_config.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found camera config at: {path}")
                return path
        
        logger.warning("No camera config file found, will create default")
        return "camera_config.json"
    
    def load_config(self) -> bool:
        """Load camera configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
                logger.info(f"Loaded camera config from {self.config_file}")
                return True
            else:
                logger.warning(f"Config file {self.config_file} not found")
                self.config_data = self._create_default_config()
                return False
        except Exception as e:
            logger.error(f"Error loading camera config: {e}")
            self.config_data = self._create_default_config()
            return False
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration if no file exists"""
        return {
            "cameras": [],
            "default_settings": {
                "frame_rate": 10,
                "resolution": "1080p", 
                "detection_enabled": True,
                "confidence_threshold": 0.7
            }
        }
    
    def get_cameras(self) -> List[Dict[str, Any]]:
        """Get all configured cameras"""
        if not self.config_data:
            return []
        return self.config_data.get("cameras", [])
    
    def get_camera_by_id(self, camera_id: int) -> Optional[Dict[str, Any]]:
        """Get camera configuration by ID"""
        cameras = self.get_cameras()
        for camera in cameras:
            if camera.get("id") == camera_id:
                return camera
        return None
    
    def get_camera_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get camera configuration by name"""
        cameras = self.get_cameras()
        for camera in cameras:
            if camera.get("name") == name:
                return camera
        return None
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default camera settings"""
        if not self.config_data:
            return {}
        return self.config_data.get("default_settings", {})
    
    def get_rtsp_fallback_paths(self) -> List[str]:
        """Get list of RTSP fallback paths to try"""
        if not self.config_data:
            return ["/stream1", "/stream2"]
        return self.config_data.get("rtsp_fallback_paths", ["/stream1", "/stream2"])
    
    def update_camera_rtsp_url(self, camera_id: int, new_rtsp_url: str) -> bool:
        """Update RTSP URL for a camera"""
        try:
            cameras = self.get_cameras()
            for camera in cameras:
                if camera.get("id") == camera_id:
                    camera["rtsp_url"] = new_rtsp_url
                    self.save_config()
                    logger.info(f"Updated camera {camera_id} RTSP URL to: {new_rtsp_url}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating camera RTSP URL: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            logger.info(f"Saved camera config to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving camera config: {e}")
            return False
    
    def reload_config(self) -> bool:
        """Reload configuration from file"""
        return self.load_config()

# Global camera config service instance
camera_config_service = CameraConfigService()
