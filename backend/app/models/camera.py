from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rtsp_url = Column(String(500), nullable=False)
    location = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_recording = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Camera settings
    frame_rate = Column(Integer, default=10)
    resolution = Column(String(50), default="1080p")
    detection_enabled = Column(Boolean, default=True)
    
    # Status information
    status = Column(String(50), default="offline")  # online, offline, error
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Camera(id={self.id}, name='{self.name}', status='{self.status}')>" 