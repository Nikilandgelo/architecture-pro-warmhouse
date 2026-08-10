from fastapi import APIRouter

from .scenarios import scenarios_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(scenarios_router, prefix="/scenarios", tags=["Scenarios"])
