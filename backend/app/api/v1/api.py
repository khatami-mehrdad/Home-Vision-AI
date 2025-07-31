from fastapi import APIRouter

from app.api.v1.endpoints import cameras, events, notifications, auth

api_router = APIRouter()

api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"]) 