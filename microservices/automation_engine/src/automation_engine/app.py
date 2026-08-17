from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.asgi import make_ping_asgi, make_asyncapi_asgi
from faststream.nats import NatsBroker
from faststream.specification import AsyncAPI

from automation_engine.adapters.nats import (
    devices_kv_store,
    error_callback,
    disconnected_callback,
    closed_callback,
    reconnected_callback
)
from automation_engine.api import api_router
from automation_engine.broker.routers import commands_router, events_router
from automation_engine.loggers import service_logger
from automation_engine.settings import settings

broker = NatsBroker(
    servers=settings.nats_url,
    name="Automation Engine",
    error_cb=error_callback,
    disconnected_cb=disconnected_callback,
    closed_cb=closed_callback,
    reconnected_cb=reconnected_callback
)
broker.include_router(commands_router)
broker.include_router(events_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    service_logger.info("Starting FastAPI, FastStream apps")
    await devices_kv_store.startup()
    async with broker:
        await broker.start()
        yield

    service_logger.info("Stopping FastAPI, FastStream apps")
    await devices_kv_store.shutdown()

app = FastAPI(
    title="Automation Engine API",
    version="1.0",
    contact={
        "name": "Nikita Selivanov",
        "email": "niki_landgelo@outlook.com"
    },
    lifespan=lifespan,
)
app.include_router(api_router)

app.mount("/health", make_ping_asgi(broker, timeout=5.0))
app.mount(
    "/asyncapi",
    make_asyncapi_asgi(
        AsyncAPI(
            broker,
            title="Automation Engine Broker",
            version="1.0",
            contact={
                "name": "Nikita Selivanov",
                "email": "niki_landgelo@outlook.com"
            },
        ),
        try_it_out_path=None
    )
)
