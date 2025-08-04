from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Home-Vision-AI"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/homevision"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS_FILE: str = "app/config/home-vision-ai-firebase-adminsdk-fbsvc-0ac8a1f589.json"
    FIREBASE_PROJECT_ID: Optional[str] = None
    
    # Camera Configuration
    CAMERA_RTSP_TIMEOUT: int = 30
    CAMERA_FRAME_RATE: int = 10
    CAMERA_RESOLUTION: str = "1080p"
    
    # AI Detection
    DETECTION_CONFIDENCE_THRESHOLD: float = 0.7
    DETECTION_MODEL_PATH: Optional[str] = None
    
    # Video Storage
    VIDEO_STORAGE_PATH: str = "./static/videos"
    MAX_VIDEO_SIZE_MB: int = 100
    
    # Notification Settings
    NOTIFICATION_COOLDOWN_MINUTES: int = 5
    MAX_NOTIFICATIONS_PER_HOUR: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 