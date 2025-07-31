import firebase_admin
from firebase_admin import credentials, messaging
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from app.core.config import settings
from app.models.event import Event

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.app = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            if settings.FIREBASE_CREDENTIALS_FILE:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
                self.app = firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
            else:
                logger.warning("Firebase credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
    
    async def send_notification(
        self,
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None,
        topic: Optional[str] = None,
        tokens: Optional[List[str]] = None
    ) -> bool:
        """Send push notification via Firebase"""
        if not self.app:
            logger.error("Firebase not initialized")
            return False
        
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                topic=topic,
                tokens=tokens
            )
            
            response = messaging.send(message)
            logger.info(f"Notification sent successfully: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
    
    async def send_event_notification(self, event: Event, camera_name: str) -> bool:
        """Send notification for a detection event"""
        title = f"Detection Alert - {event.object_type.title()}"
        body = f"{event.object_type.title()} detected on {camera_name} camera"
        
        data = {
            "event_id": str(event.id),
            "camera_id": str(event.camera_id),
            "object_type": event.object_type,
            "confidence": str(event.confidence),
            "timestamp": event.timestamp.isoformat() if event.timestamp else ""
        }
        
        return await self.send_notification(
            title=title,
            body=body,
            data=data,
            topic="detection_events"
        )
    
    async def send_camera_status_notification(
        self,
        camera_name: str,
        status: str,
        error_message: Optional[str] = None
    ) -> bool:
        """Send notification for camera status changes"""
        title = f"Camera Status - {camera_name}"
        body = f"Camera {camera_name} is now {status}"
        
        if error_message:
            body += f": {error_message}"
        
        data = {
            "camera_name": camera_name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        return await self.send_notification(
            title=title,
            body=body,
            data=data,
            topic="camera_status"
        )
    
    async def send_system_notification(
        self,
        title: str,
        body: str,
        priority: str = "normal"
    ) -> bool:
        """Send system-wide notification"""
        data = {
            "type": "system",
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        }
        
        return await self.send_notification(
            title=title,
            body=body,
            data=data,
            topic="system_notifications"
        )
    
    def subscribe_to_topic(self, tokens: List[str], topic: str) -> bool:
        """Subscribe devices to a topic"""
        if not self.app:
            return False
        
        try:
            response = messaging.subscribe_to_topic(tokens, topic)
            logger.info(f"Subscribed {response.success_count} devices to topic {topic}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to topic: {e}")
            return False
    
    def unsubscribe_from_topic(self, tokens: List[str], topic: str) -> bool:
        """Unsubscribe devices from a topic"""
        if not self.app:
            return False
        
        try:
            response = messaging.unsubscribe_from_topic(tokens, topic)
            logger.info(f"Unsubscribed {response.success_count} devices from topic {topic}")
            return True
        except Exception as e:
            logger.error(f"Failed to unsubscribe from topic: {e}")
            return False

# Global notification service instance
notification_service = NotificationService() 