# DeGirum Direct Stream Processing Setup Guide

This guide shows you how to set up DeGirum AI detection for your Home-Vision-AI system using direct RTSP stream processing, based on the [DeGirum object detection video stream example](https://github.com/DeGirum/PySDKExamples/blob/main/examples/singlemodel/object_detection_video_stream.ipynb).

## Prerequisites

1. **DeGirum Account**: Sign up at [https://cs.degirum.com/](https://cs.degirum.com/)
2. **API Token**: Get your DeGirum token from the dashboard

## Installation

### 1. Install DeGirum SDK and Tools

```bash
cd backend
pip install degirum degirum_tools
```

### 2. Configure Your Token

Edit `/backend/app/services/ai_detection_service.py` and replace:

```python
your_token = "YOUR_DEGIRUM_TOKEN_HERE"  # Replace with your actual token
```

With your actual DeGirum token from [https://cs.degirum.com/](https://cs.degirum.com/).

## How It Works

### Direct RTSP Stream Processing

Your RTSP camera streams are now processed directly by DeGirum:

1. **Stream Connection**: DeGirum connects directly to your RTSP stream using `degirum_tools.open_video_stream()`
2. **AI Processing**: Each frame is processed by DeGirum's YOLOv8 model via `degirum_tools.predict_stream()`
3. **Image Overlay**: DeGirum returns `inference_result.image_overlay` with detection boxes and labels
4. **Smart NVR**: Object tracking, zone detection, and event recording on top of DeGirum detections
5. **Web Display**: The processed frames with AI overlays are displayed in your web app

### Available Endpoints

- `GET /api/v1/cameras/{camera_id}/detections` - Get latest AI detection results
- `GET /api/v1/cameras/{camera_id}/frame` - Get camera frame with AI overlays

### Detection Objects

The YOLOv8 model can detect 80 different object classes including:
- People
- Cats, dogs, and other animals
- Vehicles (cars, trucks, motorcycles)
- Common objects (chairs, bottles, phones, etc.)

## Customization

### 1. Change AI Model

Edit `ai_detection_service.py` to use different models:

```python
# For different object detection models:
self.degirum_model = dg.load_model(
    model_name="yolov8s_relu6_coco--640x640_quant_n2x_orca1_1",  # Larger model
    # or
    model_name="yolov8n_relu6_coco--320x320_quant_n2x_orca1_1",  # Smaller/faster model
    inference_host_address="@cloud",
    zoo_url="degirum/public",
    token=your_token,
)
```

### 2. Add Custom Detection Lines

```python
# Example: Add a detection line across the camera view
detection_line = (100, 300, 500, 300)  # x1, y1, x2, y2
processed_frame = ai_detection_service.add_custom_detection_line(
    frame, detection_line, "Entry Detection"
)

# Check for line crossings
crossings = ai_detection_service.check_line_crossing(detections, detection_line)
```

### 3. Filter Specific Objects

```python
# In ai_detection_service.py, modify _run_degirum_detection:
# Only detect people and cats
allowed_objects = ["person", "cat"]
if object_type not in allowed_objects:
    continue
```

### 4. Confidence Threshold

Adjust detection sensitivity:

```python
# In ai_detection_service.py
self.confidence_threshold = 0.5  # Lower = more detections, higher = fewer false positives
```

## Local vs Cloud Inference

### Cloud Inference (Default)
```python
inference_host_address="@cloud"  # Uses DeGirum cloud servers
```

### Local Inference (Requires DeGirum hardware)
```python
inference_host_address="localhost:8080"  # Uses local DeGirum device
```

## Troubleshooting

### Common Issues

1. **"DeGirum SDK not installed"**
   ```bash
   pip install degirum
   ```

2. **"Failed to initialize DeGirum model"**
   - Check your token is correct
   - Ensure internet connection for cloud inference
   - Verify model name exists in DeGirum zoo

3. **"Token authentication failed"**
   - Get a new token from [https://cs.degirum.com/](https://cs.degirum.com/)
   - Make sure token has proper permissions

### Fallback Mode

If DeGirum is not available, the system automatically falls back to simple color-based detection for testing purposes.

## Performance Tips

1. **Model Selection**: Use smaller models (yolov8n) for faster processing
2. **Frame Rate**: Lower camera frame rate for better AI processing
3. **Resolution**: Use 640x640 or lower for faster inference
4. **Local Inference**: Use DeGirum hardware for lowest latency

## Integration Examples

### React Frontend Integration

```javascript
// Get detection results
const response = await fetch(`/api/v1/cameras/1/detections`);
const data = await response.json();

// Display detections
data.detections.forEach(detection => {
    console.log(`Detected: ${detection.object_type} (${detection.confidence})`);
});
```

### Event Triggers

```python
# In your custom code, trigger events based on detections
for detection in detections:
    if detection["object_type"] == "person" and detection["confidence"] > 0.8:
        # Send notification
        # Start recording
        # Trigger alarm
        pass
```

## Next Steps

1. Get your DeGirum token and update the configuration
2. Test with your camera feed
3. Customize detection parameters for your use case
4. Add custom detection lines or zones
5. Integrate with your notification system

For more examples, check the [DeGirum PySDK Examples](https://github.com/DeGirum/PySDKExamples) repository.
