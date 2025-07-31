from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    
    # Detection information
    object_type = Column(String(50), nullable=False)  # cat, human, unknown
    confidence = Column(Float, nullable=False)
    bounding_box = Column(Text)  # JSON string of coordinates
    
    # Video information
    video_path = Column(String(500), nullable=True)
    thumbnail_path = Column(String(500), nullable=True)
    duration_seconds = Column(Float, default=0.0)
    
    # Event metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_notified = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Additional data
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    def __repr__(self):
        return f"<Event(id={self.id}, camera_id={self.camera_id}, object_type='{self.object_type}', confidence={self.confidence})>" 