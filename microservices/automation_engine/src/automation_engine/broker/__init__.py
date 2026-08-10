from .routers import commands_router, events_router
from .telemetry import telemetry_router

events_router.include_router(telemetry_router, prefix=".telemetry")
