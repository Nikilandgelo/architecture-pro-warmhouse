from faststream.nats import NatsRouter

from telemetry.adapters.nats import EVENTS_STREAM

events_router = NatsRouter(prefix=f"{EVENTS_STREAM.name}")
