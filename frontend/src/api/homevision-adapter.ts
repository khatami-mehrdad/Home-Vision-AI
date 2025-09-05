// Home Vision AI Backend Adapter
// This file adapts the Home Vision AI backend API to work with Frigate's UI expectations

import axios from 'axios';

// Configuration for Home Vision AI backend
const HOME_VISION_API_BASE = '/api/v1';

// Type definitions to match what Frigate UI expects
export interface FrigateConfig {
  cameras: Record<string, CameraConfig>;
  mqtt?: any;
  detect?: any;
  record?: any;
  snapshots?: any;
  go2rtc?: any;
  ffmpeg?: any;
  objects?: any;
  motion?: any;
  audio?: any;
  ui?: any;
  telemetry?: any;
  version?: string;
  service_version?: string;
  safe_mode?: boolean;
}

export interface CameraConfig {
  name: string;
  enabled: boolean;
  ffmpeg: {
    inputs: Array<{
      path: string;
      roles: string[];
    }>;
  };
  detect?: {
    enabled: boolean;
    width: number;
    height: number;
    fps: number;
  };
  record?: {
    enabled: boolean;
    retain: {
      days: number;
      mode: string;
    };
  };
  snapshots?: {
    enabled: boolean;
    timestamp: boolean;
    bounding_box: boolean;
    crop: boolean;
    height: number;
  };
  objects?: {
    track: string[];
    filters: Record<string, any>;
  };
  zones?: Record<string, any>;
  motion?: any;
  audio?: any;
  live?: {
    stream_name: string;
    height: number;
    quality: number;
  };
  ui?: {
    order: number;
    dashboard: boolean;
  };
}

// Home Vision AI camera response type
interface HomeVisionCamera {
  id: number;
  name: string;
  rtsp_url: string;
  location?: string;
  status: 'online' | 'offline' | 'error';
  resolution?: string;
  frame_rate?: number;
  is_recording?: boolean;
  last_seen?: string;
  model?: string;
  zone?: string;
}

// Adapter class to transform Home Vision AI data to Frigate format
export class HomeVisionAdapter {
  
  // Convert Home Vision AI cameras to Frigate config format
  static async getFrigateConfig(): Promise<FrigateConfig> {
    try {
      // Fetch cameras from Home Vision AI backend
      const response = await axios.get(`${HOME_VISION_API_BASE}/cameras/`);
      const cameras: HomeVisionCamera[] = response.data;
      
      // Transform to Frigate config format
      const frigateConfig: FrigateConfig = {
        cameras: {},
        version: "0.14.0", // Mock version
        service_version: "1.0.0",
        safe_mode: false,
        ui: {
          live_mode: "mse",
          timezone: "America/New_York",
          use_experimental: false,
        },
        mqtt: {
          enabled: false,
        },
        detect: {
          enabled: true,
          width: 1280,
          height: 720,
          fps: 5,
        },
        record: {
          enabled: true,
          retain: {
            days: 7,
            mode: "motion"
          }
        },
        snapshots: {
          enabled: true,
          timestamp: true,
          bounding_box: true,
          crop: false,
          height: 270
        },
        objects: {
          track: ["person", "cat", "car"],
          filters: {
            person: {
              min_area: 5000,
              max_area: 100000,
              threshold: 0.7
            },
            cat: {
              min_area: 1000,
              max_area: 50000,
              threshold: 0.7
            },
            car: {
              min_area: 10000,
              max_area: 200000,
              threshold: 0.7
            }
          }
        }
      };

      // Convert each camera
      cameras.forEach((camera, index) => {
        frigateConfig.cameras[camera.name] = {
          name: camera.name,
          enabled: camera.status === 'online',
          ffmpeg: {
            inputs: [
              {
                path: camera.rtsp_url,
                roles: ["detect", "record"]
              }
            ]
          },
          detect: {
            enabled: true,
            width: 1280,
            height: 720,
            fps: camera.frame_rate || 5
          },
          record: {
            enabled: camera.is_recording || false,
            retain: {
              days: 7,
              mode: "motion"
            }
          },
          snapshots: {
            enabled: true,
            timestamp: true,
            bounding_box: true,
            crop: false,
            height: 270
          },
          objects: {
            track: ["person", "cat", "car"],
            filters: {}
          },
          zones: {},
          live: {
            stream_name: camera.name.toLowerCase().replace(/\s+/g, '_'),
            height: 720,
            quality: 8
          },
          ui: {
            order: index,
            dashboard: true
          }
        };
      });

      return frigateConfig;
    } catch (error) {
      console.error('Error fetching Home Vision AI config:', error);
      // Return minimal config on error
      return {
        cameras: {},
        version: "0.14.0",
        safe_mode: true
      };
    }
  }

  // Get camera stats (mock data for now)
  static async getStats() {
    try {
      const response = await axios.get(`${HOME_VISION_API_BASE}/cameras/`);
      const cameras: HomeVisionCamera[] = response.data;
      
      return {
        service: {
          uptime: Date.now() / 1000 - 3600, // 1 hour uptime
          version: "1.0.0",
          latest_version: "1.0.0",
          storage: {
            "/media/frigate/clips": {
              total: 1000000000, // 1GB
              used: 500000000,   // 500MB
              free: 500000000    // 500MB
            }
          }
        },
        cameras: cameras.reduce((acc, camera) => {
          acc[camera.name] = {
            camera_fps: camera.frame_rate || 5,
            capture_pid: camera.status === 'online' ? 1234 : null,
            detection_fps: camera.status === 'online' ? 2.5 : 0,
            pid: camera.status === 'online' ? 1234 : null,
            process_fps: camera.status === 'online' ? 5 : 0,
            skipped_fps: 0,
            detection_enabled: true,
            detection_frame: Date.now() / 1000
          };
          return acc;
        }, {} as Record<string, any>),
        detectors: {
          cpu: {
            detection_start: 0,
            inference_speed: 100,
            pid: 1234
          }
        },
        gpu_usages: {},
        processes: {}
      };
    } catch (error) {
      console.error('Error fetching stats:', error);
      return {
        service: { uptime: 0, version: "1.0.0" },
        cameras: {},
        detectors: {},
        gpu_usages: {},
        processes: {}
      };
    }
  }

  // Get events (mock for now - you'll need to implement this in your backend)
  static async getEvents(_params: any = {}) {
    // This would need to be implemented in your backend
    // For now, return empty array
    return [];
  }

  // Get recordings (mock for now)
  static async getRecordings(_camera: string, _date: string) {
    return [];
  }

  // Setup API interceptor to handle Frigate API calls
  static setupApiInterceptor() {
    // For now, we'll let the API calls go through normally
    // The backend adapter will handle the translation
    console.log('Home Vision AI adapter initialized');
  }
}

// Initialize the adapter
HomeVisionAdapter.setupApiInterceptor();
