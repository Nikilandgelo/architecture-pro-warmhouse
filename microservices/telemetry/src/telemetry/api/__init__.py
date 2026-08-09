from fastapi import APIRouter

from .telemetry import telemetry_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(telemetry_router, prefix="/telemetry", tags=["Telemetry"])
