from faststream.nats import NatsRouter, PullSub

from automation_engine.adapters.nats import (
    EVENTS_STREAM,
    BASE_CONSUMER_CONFIG,
    MAX_TASKS_PER_WORKER
)
from automation_engine.entities import TelemetryPayload
from automation_engine.handlers import TelemetryHandler
from automation_engine.settings import settings

telemetry_router = NatsRouter()

@telemetry_router.subscriber(
    subject="",
    durable=f"{EVENTS_STREAM.name}-telemetry-pull-consumer",
    stream=EVENTS_STREAM,
    pull_sub=PullSub(batch_size=settings.max_tasks_per_worker, timeout=0.5),
    config=BASE_CONSUMER_CONFIG,
    max_workers=settings.max_tasks_per_worker,
    title="Telemetry Events Handler"
)
async def handle_telemetry_event(payload: TelemetryPayload):
    async with MAX_TASKS_PER_WORKER:
        await TelemetryHandler.process_telemetry_event(payload=payload)
