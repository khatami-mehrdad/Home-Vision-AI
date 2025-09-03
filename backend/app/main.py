from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import logging

from app.api.v1.api import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Home-Vision-AI API",
    description="AI-powered home security camera system",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files for video storage
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    """Initialize services and auto-start camera streams on server startup"""
    logger.info("🚀 Starting Home-Vision-AI backend...")
    
    # Import here to avoid circular imports
    from app.database import create_tables
    from app.services.camera_service import camera_service
    
    try:
        # Create database tables
        create_tables()
        logger.info("✅ Database tables created/verified")
        
        # Auto-start camera streams after a short delay
        async def auto_start_cameras():
            await asyncio.sleep(3)  # Wait for everything to initialize
            try:
                # Load camera config and start streams
                import os
                import json
                
                config_paths = [
                    "camera_config.json",
                    "../camera_config.json", 
                    "../../camera_config.json"
                ]
                
                config = {}
                for config_path in config_paths:
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            full_config = json.load(f)
                            if "cameras" in full_config:
                                for camera in full_config["cameras"]:
                                    if camera.get("is_active", True):
                                        # Create simple camera object
                                        class SimpleCamera:
                                            def __init__(self, id, name, rtsp_url):
                                                self.id = id
                                                self.name = name
                                                self.rtsp_url = rtsp_url
                                        
                                        cam = SimpleCamera(
                                            camera["id"],
                                            camera["name"], 
                                            camera["rtsp_url"]
                                        )
                                        
                                        logger.info(f"🎥 Auto-starting camera {cam.id}: {cam.name}")
                                        success = await camera_service.start_camera_stream(cam)
                                        if success:
                                            logger.info(f"✅ Camera {cam.id} started successfully")
                                        else:
                                            logger.error(f"❌ Failed to start camera {cam.id}")
                        break
                else:
                    logger.warning("⚠️ No camera config file found for auto-start")
                    
            except Exception as e:
                logger.error(f"💥 Error auto-starting cameras: {e}")
        
        # Start cameras in background
        asyncio.create_task(auto_start_cameras())
        
    except Exception as e:
        logger.error(f"💥 Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on server shutdown"""
    logger.info("🛑 Shutting down Home-Vision-AI backend...")
    
    try:
        from app.services.camera_service import camera_service
        
        # Stop all active camera streams
        active_cameras = list(camera_service.active_streams.keys())
        for camera_id in active_cameras:
            logger.info(f"🛑 Stopping camera {camera_id}")
            await camera_service.stop_camera_stream(camera_id)
            
        logger.info("✅ All camera streams stopped")
        
    except Exception as e:
        logger.error(f"💥 Error during shutdown: {e}")

@app.get("/")
async def root():
    return {"message": "Home-Vision-AI API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    try:
        from app.services.camera_service import camera_service
        return {"status": "healthy", "cameras_active": len(camera_service.active_streams)}
    except Exception:
        return {"status": "healthy", "cameras_active": 0}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 