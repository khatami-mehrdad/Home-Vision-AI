# RTSP Camera Test Script

A comprehensive tool for testing RTSP camera connectivity and displaying video feeds. Supports both local and remote SSH environments with video creation capabilities.

## Features

- Test single or multiple RTSP camera connections
- Display live camera feeds
- Headless mode for remote SSH sessions
- Save frames to files for analysis
- **Create videos from saved frames**
- Interactive mode for easy testing
- Support for camera configuration files

## Usage

### Basic Testing

```bash
# Test a single camera connection
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --name "Front Door"

# Test multiple cameras from config file
python tests/rtsp_test.py --config tests/camera_config.json
```

### Display Camera Feeds

```bash
# Display camera feed locally (requires display)
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --display --duration 30

# Display in headless mode (for remote SSH)
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --display --headless --duration 30

# Save frames to files in headless mode
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --display --headless --save-frames --output-dir "camera_frames" --duration 30

# Save frames AND create video automatically
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --display --headless --save-frames --create-video --video-fps 15 --duration 60
```

### Video Creation

```bash
# Create video from existing frames directory
python tests/rtsp_test.py --frames-to-video "frames/Camera" --video-output "camera_recording.mp4" --video-fps 10

# Create video with custom FPS
python tests/rtsp_test.py --frames-to-video "frames/Camera" --video-fps 30 --video-output "high_fps_video.mp4"
```

### Multiple Camera Testing

```bash
# Test multiple cameras from config file
python tests/rtsp_test.py --config tests/camera_config.json

# Display multiple feeds in headless mode
python tests/rtsp_test.py --config tests/camera_config.json --display --headless --save-frames

# Create videos for all cameras
python tests/rtsp_test.py --config tests/camera_config.json --display --headless --save-frames --create-video
```

## Remote SSH Usage

When working in a remote SSH session without a display, use the headless mode:

```bash
# Test camera connectivity only
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1"

# Display feed with frame saving
python tests/rtsp_test.py --url "rtsp://192.168.1.100:554/stream1" --display --headless --save-frames --duration 60

# Create video from saved frames
python tests/rtsp_test.py --frames-to-video "frames/Camera" --video-output "remote_camera.mp4"

# View saved frames and videos
ls -la frames/
ls -la *.mp4
```

## Command Line Options

- `--url`: Single RTSP URL to test
- `--name`: Camera name (default: "Camera")
- `--display`: Display video feed
- `--duration`: Display duration in seconds (default: 30)
- `--config`: JSON file with multiple camera configurations
- `--headless`: Run in headless mode (no GUI windows)
- `--save-frames`: Save frames to files (headless mode)
- `--output-dir`: Output directory for saved frames (default: "frames")
- `--create-video`: Create video from saved frames
- `--video-fps`: FPS for created video (default: 10)
- `--frames-to-video`: Create video from existing frames directory
- `--video-output`: Output video filename

## Video Creation Features

### Automatic Video Creation
When using `--create-video` with `--save-frames`, the script will:
1. Save frames during camera recording
2. Automatically create an MP4 video when recording completes
3. Use the camera name for the video filename

### Manual Video Creation
Create videos from previously saved frames:
```bash
python tests/rtsp_test.py --frames-to-video "frames/Camera" --video-output "my_video.mp4" --video-fps 15
```

### Video Formats
- **Output Format**: MP4 (using H.264 codec)
- **Supported Frame Formats**: JPG, JPEG, PNG
- **Frame Naming**: Must include frame numbers (e.g., `Camera_000001.jpg`)

### Video Quality Settings
- **FPS**: Configurable (default: 10 FPS)
- **Resolution**: Maintains original frame resolution
- **Codec**: H.264 for compatibility

## Configuration File Format

Create a JSON file with camera configurations:

```json
{
  "Front Door": "rtsp://192.168.1.100:554/stream1",
  "Back Yard": "rtsp://192.168.1.101:554/stream1",
  "Garage": "rtsp://192.168.1.102:554/stream1"
}
```

## Interactive Mode

Run without arguments for interactive mode:

```bash
python tests/rtsp_test.py
```

This provides a menu-driven interface for testing cameras and creating videos.

## File Structure

After running with video creation, you'll have:
```
frames/
├── Camera_000001.jpg
├── Camera_000002.jpg
├── ...
└── Camera_video.mp4
```

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check network connectivity and RTSP URL format
2. **Authentication Error**: Verify username/password in RTSP URL
3. **No Display**: Use `--headless` flag for remote SSH sessions
4. **Frame Saving**: Ensure write permissions for output directory
5. **Video Creation Failed**: Check if frames exist and have correct naming format
6. **Video Codec Issues**: Ensure OpenCV is compiled with video codec support

### RTSP URL Formats

```
rtsp://username:password@camera_ip:554/stream1
rtsp://camera_ip:554/stream1
rtsp://camera_ip:554/h264Preview_01_main
```

### Network Requirements

- Cameras must be accessible from the test machine
- Proper firewall configuration
- Correct RTSP port (usually 554)
- Network bandwidth for video streaming

### Video Creation Tips

1. **Frame Rate**: Higher FPS = smoother video but larger file size
2. **Duration**: Longer recordings = more frames = larger videos
3. **Storage**: Ensure sufficient disk space for frames and videos
4. **Naming**: Frame files must be sortable by name for correct video order 