from faststream.nats import NatsRouter

from device_management.adapters.nats import COMMANDS_STREAM, EVENTS_STREAM
from .devices import devices_router

commands_router = NatsRouter(prefix=f"{COMMANDS_STREAM.name}")
events_router = NatsRouter(prefix=f"{EVENTS_STREAM.name}")

commands_router.include_router(devices_router)
