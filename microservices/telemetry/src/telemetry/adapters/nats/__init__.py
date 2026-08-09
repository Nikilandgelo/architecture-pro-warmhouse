from faststream.nats import JStream

from telemetry.loggers import service_logger
from telemetry.settings import settings
from .kv_store import devices_kv_store

COMMANDS_STREAM: JStream = JStream(name=settings.nats_commands_stream, declare=False)
EVENTS_STREAM: JStream = JStream(name=settings.nats_events_stream, declare=False)


async def error_callback(error) -> None:
    service_logger.error(f"NATS error: {error}")

async def disconnected_callback() -> None:
    service_logger.warning("NATS disconnected")

async def closed_callback() -> None:
    service_logger.error("NATS connection closed")

async def reconnected_callback() -> None:
    service_logger.warning("NATS reconnected")
