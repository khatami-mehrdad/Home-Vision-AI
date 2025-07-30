
# Home-Vision-AI 🛡️📹  
*Edge-based AI Camera System for Home Security, Cat Detection, and Smart Automation*

## Overview

Home-Vision-AI is a smart home vision system powered by real-time object detection on edge devices. Initially built for detecting cats using RTSP-enabled wireless cameras, the project is expanding into a general-purpose security and automation platform. It runs on a small Linux-based PC with an M.2 AI accelerator (e.g., Hailo or DeGirum).

---

## Goals

- Detect pets (starting with cats) via wireless RTSP cameras
- Use edge AI acceleration for real-time inference
- Notify user via phone (push or SMS)
- Support multiple cameras simultaneously (min. 6)
- Build a modular system that can grow into home automation

---

## Phases

### ✅ Phase 1: Hardware Setup & Streaming
- [ ] Set up cameras in different locations (RTSP-ready, e.g., Tapo C200)
- [ ] Connect all cameras to the local network
- [ ] Set up small PC (e.g., Beelink) with Ubuntu
- [ ] Install AI accelerator SDK (DeGirum PySDK or Hailo)
- [ ] Test RTSP streams with GStreamer/OpenCV

### 🚧 Phase 2: MVP (Minimum Viable Product)
- [ ] Create Python module for capturing RTSP streams
- [ ] Load AI model via accelerator (cat detector)
- [ ] Run detection on incoming frames (10 FPS, 1080p or lower)
- [ ] Add simple logic to trigger detection events
- [ ] Set up logging and timestamped snapshots
- [ ] Add phone notification (e.g., via Pushover, Telegram, or email)

### 🚀 Phase 3: Frontend + Usability
- [ ] Build simple web UI (Streamlit, Flask, or FastAPI + React)
- [ ] Show camera streams and recent detections
- [ ] Add settings/config interface
- [ ] Enable camera health/status monitoring

### 🌐 Phase 4: Expansion & Automation
- [ ] Add support for detection of humans / unknown objects
- [ ] Add time-based or event-based rules (e.g., alert only at night)
- [ ] Enable cloud logging or remote access (optional)
- [ ] Home assistant integration (optional)
- [ ] Optimize for multi-camera scaling (threaded or async)

---

## Project Stack

| Component     | Tool                         |
|---------------|------------------------------|
| Language      | Python (possibly C++ backend)|
| AI Inference  | DeGirum PySDK                |
| Stream Decode | OpenCV / GStreamer           |
| Notifications | Pushover / Telegram / Twilio |
| UI            | Streamlit / Flask / React    |
| Platform      | Ubuntu + AI Edge PC          |

---

## Getting Started

> ⚠️ This section will be filled out in detail after Phase 1 setup is complete.

---

## License

Apache License

---

## Contributions

Solo project for now. If you're interested in contributing, feel free to open an issue or fork the repo.

