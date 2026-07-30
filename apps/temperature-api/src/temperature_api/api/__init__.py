from fastapi import APIRouter

from .temperature import temperature_router

api_router = APIRouter()
api_router.include_router(temperature_router, prefix="/temperature", tags=["temperature"])
