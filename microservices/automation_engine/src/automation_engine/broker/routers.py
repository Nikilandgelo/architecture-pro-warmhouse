from faststream.nats import NatsRouter

from automation_engine.adapters.nats import COMMANDS_STREAM, EVENTS_STREAM

commands_router = NatsRouter(prefix=COMMANDS_STREAM.name)
events_router = NatsRouter(prefix=EVENTS_STREAM.name)
