from fastapi import APIRouter

from .allowed_commands import allowed_commands_router
from .device_types import device_types_router
from .devices import devices_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(device_types_router, prefix="/device-types", tags=["Device Types"])
api_router.include_router(devices_router, prefix="/devices", tags=["Devices"])
api_router.include_router(
    allowed_commands_router, prefix="/allowed-commands", tags=["Allowed Commands"]
)
