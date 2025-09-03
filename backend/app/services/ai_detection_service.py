import cv2
import numpy as np
import logging
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class SmartNVRDetectionService:
    """Enhanced DeGirum-based Smart NVR Detection Service with tracking and event recording"""
    
    def __init__(self):
        self.detection_enabled = True
        self.confidence_threshold = 0.7
        self.degirum_model = None
        
        # Smart NVR capabilities
        self.object_trackers = {}  # Camera-wise object tracking
        self.detection_zones = {}  # Camera-wise detection zones
        self.event_history = defaultdict(deque)  # Event recording per camera
        self.alert_cooldowns = {}  # Prevent spam alerts
        
        # Tracking parameters
        self.max_track_age = 30  # frames
        self.min_track_hits = 3  # minimum detections to confirm track
        self.track_distance_threshold = 100  # pixels
        
        # Event recording parameters
        self.record_buffer_seconds = 10  # seconds before/after event
        self.max_events_per_camera = 100
        
        # Initialize DeGirum model
        self._initialize_degirum_model()
        logger.info("Smart NVR Detection Service initialized with DeGirum")
    
    def _initialize_degirum_model(self):
        """Initialize DeGirum AI model for video stream processing"""
        try:
            import degirum as dg
            import degirum_tools
            
            # You need to set your DeGirum token here
            # Get your token from https://cs.degirum.com/
            your_token = degirum_tools.get_token()  # Replace with your actual token
            
            # Load YOLOv8 model for object detection
            self.degirum_model = dg.load_model(
                model_name="yolov8n_relu6_coco--640x640_quant_n2x_orca1_1",
                inference_host_address="@cloud",  # Use cloud inference
                zoo_url="degirum/public",
                token=your_token,
            )
            
            # Store degirum_tools for stream processing
            self.degirum_tools = degirum_tools
            
            logger.info("DeGirum model and tools loaded successfully")
            
        except ImportError as e:
            logger.warning(f"DeGirum SDK not installed: {e}. Install with: pip install degirum")
            self.degirum_model = None
            self.degirum_tools = None
        except Exception as e:
            logger.error(f"Failed to initialize DeGirum model: {e}")
            logger.info("Please set your DeGirum token in ai_detection_service.py")
            self.degirum_model = None
            self.degirum_tools = None
    
    def process_frame(self, frame: np.ndarray, camera_id: int) -> Dict[str, Any]:
        """
        Enhanced Smart NVR frame processing with tracking and event detection
        
        Args:
            frame: OpenCV frame (numpy array)
            camera_id: ID of the camera
            
        Returns:
            Dictionary containing detection results, tracking data, and events
        """
        if not self.detection_enabled:
            return {"detections": [], "processed_frame": frame, "events": [], "tracks": []}
        
        try:
            current_time = datetime.now()
            
            # Run AI detection
            detections = self._run_custom_detection(frame)
            
            # Update object tracking
            tracks = self._update_tracking(camera_id, detections, current_time)
            
            # Check for events (zone violations, new objects, etc.)
            events = self._check_events(camera_id, detections, tracks, current_time)
            
            # Draw detection results, tracks, and zones on frame
            processed_frame = self._draw_smart_nvr_overlays(frame.copy(), detections, tracks, camera_id)
            
            # Update event history
            if events:
                self._record_events(camera_id, events, current_time)
            
            return {
                "detections": detections,
                "tracks": tracks,
                "events": events,
                "processed_frame": processed_frame,
                "timestamp": current_time,
                "camera_id": camera_id
            }
            
        except Exception as e:
            logger.error(f"Error processing frame for camera {camera_id}: {e}")
            return {"detections": [], "processed_frame": frame, "events": [], "tracks": []}
    
    def _run_custom_detection(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        DeGirum AI detection logic only
        """
        detections = []
        
        # Only use DeGirum model - no fallback
        if self.degirum_model is not None:
            detections = self._run_degirum_detection(frame)
        else:
            logger.warning("DeGirum model not available - no detections will be performed")
        
        return detections
    
    def create_degirum_stream_processor(self, rtsp_url: str):
        """
        Create a DeGirum stream processor for direct RTSP processing
        Based on DeGirum's object_detection_video_stream example
        """
        if self.degirum_model is None or self.degirum_tools is None:
            logger.error("DeGirum model or tools not available")
            return None
        
        try:
            # Create video source from RTSP URL
            video_source = self.degirum_tools.open_video_stream(rtsp_url)
            logger.info(f"Created DeGirum video stream processor for: {rtsp_url}")
            return video_source
        except Exception as e:
            logger.error(f"Failed to create DeGirum stream processor: {e}")
            return None
    
    def process_degirum_stream(self, rtsp_url: str, camera_id: int):
        """
        Process DeGirum video stream directly from RTSP URL
        Based on DeGirum's predict_stream example
        """
        if self.degirum_model is None or self.degirum_tools is None:
            logger.error("DeGirum model or tools not available")
            return
        
        try:
            # Use DeGirum's predict_stream with RTSP URL directly
            for inference_result in self.degirum_tools.predict_stream(self.degirum_model, rtsp_url):
                # Debug: Check what's inside inference_result
                logger.info(f"DeGirum inference_result type: {type(inference_result)}")
                logger.info(f"DeGirum inference_result attributes: {dir(inference_result)}")
                
                # Extract detection data from DetectionResults object
                detections = []
                
                # Try to access results - check different possible attributes
                results_list = None
                if hasattr(inference_result, 'results'):
                    results_list = inference_result.results
                    logger.info(f"Found .results attribute with {len(results_list)} items")
                elif hasattr(inference_result, '__iter__'):
                    try:
                        results_list = list(inference_result)
                        logger.info(f"Inference result is iterable with {len(results_list)} items")
                    except:
                        logger.warning("Failed to iterate over inference_result")
                else:
                    logger.warning("No .results attribute and not iterable")
                
                if results_list:
                    # inference_result is a DetectionResults object, iterate through its detections
                    for detection in results_list:
                        bbox = detection.bbox
                        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])
                        
                        confidence = float(detection.score)
                        if confidence < self.confidence_threshold:
                            continue
                        
                        object_type = str(detection.label)
                        
                        detections.append({
                            "object_type": object_type,
                            "confidence": confidence,
                            "bounding_box": [x, y, w, h],
                            "center": [x + w//2, y + h//2],
                            "area": w * h,
                            "degirum_data": {
                                "class_id": detection.category_id,
                                "bbox_normalized": bbox,
                                "score": detection.score
                            }
                        })
                
                # Get the image with overlays (this is what we want to display)
                processed_frame = inference_result.image_overlay
                
                # Update tracking and events
                current_time = datetime.now()
                tracks = self._update_tracking(camera_id, detections, current_time)
                events = self._check_events(camera_id, detections, tracks, current_time)
                
                # Record events
                if events:
                    self._record_events(camera_id, events, current_time)
                
                yield {
                    "detections": detections,
                    "tracks": tracks,
                    "events": events,
                    "processed_frame": processed_frame,  # DeGirum's image_overlay
                    "timestamp": current_time,
                    "camera_id": camera_id
                }
                
        except Exception as e:
            logger.error(f"Error in DeGirum stream processing: {e}")
    
    def _update_tracking(self, camera_id: int, detections: List[Dict[str, Any]], current_time: datetime) -> List[Dict[str, Any]]:
        """Update object tracking for Smart NVR capabilities"""
        if camera_id not in self.object_trackers:
            self.object_trackers[camera_id] = []
        
        tracks = self.object_trackers[camera_id]
        active_tracks = []
        
        # Update existing tracks
        for track in tracks:
            track['age'] += 1
            track['matched'] = False
        
        # Match detections to tracks
        for detection in detections:
            det_center = detection['center']
            best_track = None
            best_distance = float('inf')
            
            for track in tracks:
                if track['object_type'] == detection['object_type']:
                    distance = np.sqrt((track['center'][0] - det_center[0])**2 + 
                                     (track['center'][1] - det_center[1])**2)
                    if distance < self.track_distance_threshold and distance < best_distance:
                        best_distance = distance
                        best_track = track
            
            if best_track:
                # Update existing track
                best_track['center'] = det_center
                best_track['bounding_box'] = detection['bounding_box']
                best_track['confidence'] = detection['confidence']
                best_track['age'] = 0
                best_track['hits'] += 1
                best_track['matched'] = True
                best_track['last_seen'] = current_time
            else:
                # Create new track
                new_track = {
                    'track_id': f"{camera_id}_{current_time.timestamp()}",
                    'object_type': detection['object_type'],
                    'center': det_center,
                    'bounding_box': detection['bounding_box'],
                    'confidence': detection['confidence'],
                    'age': 0,
                    'hits': 1,
                    'matched': True,
                    'first_seen': current_time,
                    'last_seen': current_time,
                    'path': [det_center]
                }
                tracks.append(new_track)
        
        # Keep only valid tracks
        for track in tracks:
            if track['matched'] or track['age'] < self.max_track_age:
                if track['hits'] >= self.min_track_hits:
                    active_tracks.append(track)
                elif track['matched']:
                    active_tracks.append(track)
        
        self.object_trackers[camera_id] = active_tracks
        return active_tracks
    
    def _check_events(self, camera_id: int, detections: List[Dict[str, Any]], 
                     tracks: List[Dict[str, Any]], current_time: datetime) -> List[Dict[str, Any]]:
        """Check for Smart NVR events like zone violations, new objects, etc."""
        events = []
        
        # Check for zone violations
        if camera_id in self.detection_zones:
            for zone in self.detection_zones[camera_id]:
                for detection in detections:
                    if self._point_in_zone(detection['center'], zone):
                        if zone.get('restricted', False):
                            events.append({
                                'type': 'zone_violation',
                                'camera_id': camera_id,
                                'object_type': detection['object_type'],
                                'confidence': detection['confidence'],
                                'zone_name': zone['name'],
                                'timestamp': current_time,
                                'location': detection['center']
                            })
        
        # Check for new objects (first detection)
        for track in tracks:
            if track['hits'] == self.min_track_hits:  # Just confirmed as valid track
                events.append({
                    'type': 'object_detected',
                    'camera_id': camera_id,
                    'object_type': track['object_type'],
                    'confidence': track['confidence'],
                    'track_id': track['track_id'],
                    'timestamp': current_time,
                    'location': track['center']
                })
        
        # Check for loitering (object staying too long)
        for track in tracks:
            duration = (current_time - track['first_seen']).total_seconds()
            if duration > 30:  # 30 seconds threshold
                events.append({
                    'type': 'loitering_detected',
                    'camera_id': camera_id,
                    'object_type': track['object_type'],
                    'track_id': track['track_id'],
                    'duration': duration,
                    'timestamp': current_time,
                    'location': track['center']
                })
        
        # Filter events based on cooldown
        filtered_events = self._filter_events_with_cooldown(camera_id, events)
        
        return filtered_events
    
    def _point_in_zone(self, point: Tuple[int, int], zone: Dict[str, Any]) -> bool:
        """Check if a point is inside a detection zone"""
        if zone['type'] == 'rectangle':
            x, y = point
            x1, y1, x2, y2 = zone['coordinates']
            return x1 <= x <= x2 and y1 <= y <= y2
        elif zone['type'] == 'polygon':
            # Use cv2.pointPolygonTest for polygon zones
            polygon = np.array(zone['coordinates'], np.int32)
            return cv2.pointPolygonTest(polygon, point, False) >= 0
        return False
    
    def _filter_events_with_cooldown(self, camera_id: int, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter events to prevent spam alerts"""
        filtered = []
        current_time = datetime.now()
        
        for event in events:
            event_key = f"{camera_id}_{event['type']}_{event.get('object_type', '')}"
            
            if event_key not in self.alert_cooldowns:
                self.alert_cooldowns[event_key] = current_time
                filtered.append(event)
            else:
                last_alert = self.alert_cooldowns[event_key]
                if (current_time - last_alert).total_seconds() > 30:  # 30 second cooldown
                    self.alert_cooldowns[event_key] = current_time
                    filtered.append(event)
        
        return filtered
    
    def _record_events(self, camera_id: int, events: List[Dict[str, Any]], timestamp: datetime):
        """Record events for Smart NVR event history"""
        for event in events:
            self.event_history[camera_id].append({
                **event,
                'recorded_at': timestamp
            })
            
            # Maintain max events per camera
            if len(self.event_history[camera_id]) > self.max_events_per_camera:
                self.event_history[camera_id].popleft()
    
    def _draw_smart_nvr_overlays(self, frame: np.ndarray, detections: List[Dict[str, Any]], 
                                tracks: List[Dict[str, Any]], camera_id: int) -> np.ndarray:
        """Draw Smart NVR overlays including detections, tracks, and zones"""
        # Draw detection zones first
        if camera_id in self.detection_zones:
            for zone in self.detection_zones[camera_id]:
                self._draw_zone(frame, zone)
        
        # Draw detections
        for detection in detections:
            bbox = detection["bounding_box"]
            x, y, w, h = bbox
            confidence = detection["confidence"]
            obj_type = detection["object_type"]
            
            # Draw bounding box
            color = (0, 255, 0) if confidence > 0.8 else (0, 255, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw label
            label = f"{obj_type}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, (x, y - label_size[1] - 10), (x + label_size[0], y), color, -1)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        # Draw tracks
        for track in tracks:
            if track['hits'] >= self.min_track_hits:
                center = track['center']
                track_id = track['track_id']
                
                # Draw track center
                cv2.circle(frame, center, 5, (255, 0, 0), -1)
                
                # Draw track ID
                cv2.putText(frame, f"ID:{track_id[-4:]}", (center[0] + 10, center[1]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                # Draw track path if available
                if len(track.get('path', [])) > 1:
                    points = np.array(track['path'][-10:], np.int32)  # Last 10 points
                    cv2.polylines(frame, [points], False, (255, 0, 0), 2)
        
        return frame
    
    def _draw_zone(self, frame: np.ndarray, zone: Dict[str, Any]):
        """Draw detection zone on frame"""
        color = (0, 0, 255) if zone.get('restricted', False) else (255, 255, 0)
        
        if zone['type'] == 'rectangle':
            x1, y1, x2, y2 = zone['coordinates']
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        elif zone['type'] == 'polygon':
            points = np.array(zone['coordinates'], np.int32)
            cv2.polylines(frame, [points], True, color, 2)
        
        # Draw zone name
        if 'name' in zone:
            cv2.putText(frame, zone['name'], (zone['coordinates'][0], zone['coordinates'][1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    def _draw_detections(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """Draw detection results on the frame"""
        for detection in detections:
            bbox = detection["bounding_box"]
            x, y, w, h = bbox
            confidence = detection["confidence"]
            obj_type = detection["object_type"]
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw label
            label = f"{obj_type}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, (x, y - label_size[1] - 10), (x + label_size[0], y), (0, 255, 0), -1)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        return frame
    
    def add_custom_detection_line(self, frame: np.ndarray, line_coords: Tuple[int, int, int, int], 
                                 line_name: str = "Detection Line") -> np.ndarray:
        """
        Add a custom detection line to the frame
        
        Args:
            frame: OpenCV frame
            line_coords: (x1, y1, x2, y2) coordinates of the line
            line_name: Name of the detection line
            
        Returns:
            Frame with detection line drawn
        """
        x1, y1, x2, y2 = line_coords
        
        # Draw the detection line
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        
        # Add label
        cv2.putText(frame, line_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        return frame
    
    def check_line_crossing(self, detections: List[Dict[str, Any]], 
                           line_coords: Tuple[int, int, int, int]) -> List[Dict[str, Any]]:
        """
        Check if any detections cross a detection line
        
        Args:
            detections: List of detection results
            line_coords: (x1, y1, x2, y2) coordinates of the line
            
        Returns:
            List of detections that crossed the line
        """
        crossings = []
        x1, y1, x2, y2 = line_coords
        
        for detection in detections:
            center_x, center_y = detection["center"]
            
            # Simple line crossing detection (you can make this more sophisticated)
            # Check if the center point is near the line
            distance = self._point_to_line_distance(center_x, center_y, x1, y1, x2, y2)
            
            if distance < 20:  # Threshold for line crossing
                crossings.append(detection)
        
        return crossings
    
    def _point_to_line_distance(self, px: int, py: int, x1: int, y1: int, x2: int, y2: int) -> float:
        """Calculate distance from point to line"""
        A = x2 - x1
        B = y2 - y1
        C = px - x1
        D = py - y1
        
        dot = A * C + B * D
        len_sq = A * A + B * B
        
        if len_sq == 0:
            return np.sqrt(C * C + D * D)
        
        param = dot / len_sq
        
        if param < 0:
            xx, yy = x1, y1
        elif param > 1:
            xx, yy = x2, y2
        else:
            xx = x1 + param * A
            yy = y1 + param * B
        
        dx = px - xx
        dy = py - yy
        return np.sqrt(dx * dx + dy * dy)
    
    # ADD YOUR CUSTOM AI MODELS HERE:
    
    def _run_yolo_detection(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Example: YOLO detection integration
        Replace with your actual YOLO model
        """
        # Your YOLO model code here
        # net = cv2.dnn.readNet("yolo_weights.weights", "yolo_config.cfg")
        # ...
        return []
    
    def _run_degirum_detection(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        DeGirum AI model detection based on RTSP smart camera example
        """
        detections = []
        
        try:
            if self.degirum_model is None:
                return detections
            
            # Run inference on the frame
            result = self.degirum_model.predict(frame)
            
            # Process DeGirum results
            for detection in result:
                # Get bounding box coordinates
                bbox = detection.bbox
                x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])
                
                # Filter by confidence threshold
                confidence = float(detection.score)
                if confidence < self.confidence_threshold:
                    continue
                
                # Get object label
                object_type = str(detection.label)
                
                # Create detection dictionary
                detections.append({
                    "object_type": object_type,
                    "confidence": confidence,
                    "bounding_box": [x, y, w, h],
                    "center": [x + w//2, y + h//2],
                    "area": w * h,
                    "degirum_data": {
                        "class_id": detection.category_id,
                        "bbox_normalized": bbox,
                        "score": detection.score
                    }
                })
                
                logger.debug(f"DeGirum detected: {object_type} with confidence {confidence:.2f}")
            
        except Exception as e:
            logger.error(f"Error in DeGirum detection: {e}")
        
        return detections
    
    def _run_custom_model(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Your completely custom AI model
        """
        # Add your custom model here
        return []
    
    # Smart NVR Zone Management Methods
    
    def add_detection_zone(self, camera_id: int, zone_name: str, zone_type: str, 
                          coordinates: List[int], restricted: bool = False) -> bool:
        """Add a detection zone for Smart NVR capabilities"""
        try:
            if camera_id not in self.detection_zones:
                self.detection_zones[camera_id] = []
            
            zone = {
                'name': zone_name,
                'type': zone_type,  # 'rectangle' or 'polygon'
                'coordinates': coordinates,
                'restricted': restricted,
                'created_at': datetime.now()
            }
            
            self.detection_zones[camera_id].append(zone)
            logger.info(f"Added detection zone '{zone_name}' for camera {camera_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding detection zone: {e}")
            return False
    
    def remove_detection_zone(self, camera_id: int, zone_name: str) -> bool:
        """Remove a detection zone"""
        try:
            if camera_id in self.detection_zones:
                self.detection_zones[camera_id] = [
                    zone for zone in self.detection_zones[camera_id] 
                    if zone['name'] != zone_name
                ]
                logger.info(f"Removed detection zone '{zone_name}' from camera {camera_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error removing detection zone: {e}")
            return False
    
    def get_detection_zones(self, camera_id: int) -> List[Dict[str, Any]]:
        """Get all detection zones for a camera"""
        return self.detection_zones.get(camera_id, [])
    
    def get_event_history(self, camera_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get event history for Smart NVR"""
        events = list(self.event_history.get(camera_id, []))
        return events[-limit:] if events else []
    
    def get_active_tracks(self, camera_id: int) -> List[Dict[str, Any]]:
        """Get active object tracks for a camera"""
        return self.object_trackers.get(camera_id, [])
    
    def clear_camera_data(self, camera_id: int):
        """Clear all Smart NVR data for a camera"""
        if camera_id in self.object_trackers:
            del self.object_trackers[camera_id]
        if camera_id in self.detection_zones:
            del self.detection_zones[camera_id]
        if camera_id in self.event_history:
            del self.event_history[camera_id]
        
        # Clear cooldowns for this camera
        keys_to_remove = [key for key in self.alert_cooldowns.keys() if key.startswith(f"{camera_id}_")]
        for key in keys_to_remove:
            del self.alert_cooldowns[key]
    
    def get_nvr_statistics(self) -> Dict[str, Any]:
        """Get Smart NVR statistics"""
        stats = {
            'total_cameras': len(self.object_trackers),
            'active_tracks': sum(len(tracks) for tracks in self.object_trackers.values()),
            'total_zones': sum(len(zones) for zones in self.detection_zones.values()),
            'total_events': sum(len(events) for events in self.event_history.values()),
            'cameras': {}
        }
        
        for camera_id in self.object_trackers.keys():
            stats['cameras'][camera_id] = {
                'active_tracks': len(self.object_trackers.get(camera_id, [])),
                'zones': len(self.detection_zones.get(camera_id, [])),
                'recent_events': len(self.event_history.get(camera_id, []))
            }
        
        return stats

# Global Smart NVR detection service instance
ai_detection_service = SmartNVRDetectionService()

