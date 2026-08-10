from asyncio import Semaphore

from faststream.nats import JStream
from nats.js.api import ConsumerConfig, DeliverPolicy

from automation_engine.loggers import service_logger
from automation_engine.settings import settings
from .kv_store import devices_kv_store

COMMANDS_STREAM: JStream = JStream(name=settings.nats_commands_stream, declare=False)
EVENTS_STREAM: JStream = JStream(name=settings.nats_events_stream, declare=False)
MAX_TASKS_PER_WORKER: Semaphore = Semaphore(settings.max_tasks_per_worker)
BASE_CONSUMER_CONFIG: ConsumerConfig = ConsumerConfig(
    deliver_policy=DeliverPolicy.ALL,
    max_deliver=5,
)

async def error_callback(error) -> None:
    service_logger.error(f"NATS error: {error}")

async def disconnected_callback() -> None:
    service_logger.warning("NATS disconnected")

async def closed_callback() -> None:
    service_logger.error("NATS connection closed")

async def reconnected_callback() -> None:
    service_logger.warning("NATS reconnected")
