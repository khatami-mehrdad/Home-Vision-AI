from fastapi import APIRouter
import httpx

from app.api.v1.endpoints import cameras, frigate_adapter
# from app.api.v1.endpoints import events, notifications, auth

api_router = APIRouter()

api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(frigate_adapter.router, prefix="", tags=["frigate-adapter"])

@api_router.get("/go2rtc/streams/{stream_name}")
async def get_go2rtc_stream_info(stream_name: str):
    """Proxy go2rtc stream info from real go2rtc server"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:1984/api/streams")
            if response.status_code == 200:
                streams = response.json()
                if stream_name in streams:
                    stream_data = streams[stream_name]
                    # Ensure the data structure matches what the frontend expects
                    return {
                        "producers": stream_data.get("producers", []),
                        "consumers": stream_data.get("consumers") or []
                    }
                else:
                    return {
                        "producers": [],
                        "consumers": [],
                        "error": f"Stream {stream_name} not found"
                    }
            else:
                return {
                    "producers": [],
                    "consumers": [],
                    "error": "Could not fetch streams"
                }
    except Exception as e:
        return {
            "producers": [],
            "consumers": [],
            "error": f"go2rtc server not available: {str(e)}"
        }

@api_router.get("/go2rtc/streams")
async def get_all_go2rtc_streams():
    """Get all available streams from go2rtc"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:1984/api/streams")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Could not fetch streams"}
    except Exception as e:
        return {"error": f"go2rtc server not available: {str(e)}"}

# WebSocket endpoints moved to main.py for proper registration

# api_router.include_router(events.router, prefix="/events", tags=["events"])
# api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"]) 