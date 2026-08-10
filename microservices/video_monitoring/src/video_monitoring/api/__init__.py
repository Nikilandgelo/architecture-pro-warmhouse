from fastapi import APIRouter

from .archive_records import archive_records_router
from .video import video_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(video_router, prefix="/video", tags=["Video"])
api_router.include_router(
    archive_records_router, prefix="/archive-records", tags=["Archive Records"]
)
