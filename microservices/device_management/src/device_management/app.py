from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.asgi import make_ping_asgi, make_asyncapi_asgi
from faststream.nats import NatsBroker
from faststream.specification import AsyncAPI

from device_management.adapters.nats import (
    devices_kv_store,
    error_callback,
    disconnected_callback,
    closed_callback,
    reconnected_callback
)
from device_management.api import api_router
from device_management.broker import commands_router, events_router
from device_management.loggers import service_logger
from device_management.settings import settings

broker = NatsBroker(
    servers=settings.nats_url,
    name="Device Management",
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
    title="Device Management API",
    version="1.0",
    contact={
        "name": "Nikita Selivanov",
        "email": "niki_landgelo@outlook.com"
    },
    lifespan=lifespan
)
app.include_router(api_router)

app.mount("/health", make_ping_asgi(broker, timeout=5.0))
app.mount(
    "/asyncapi",
    make_asyncapi_asgi(
        AsyncAPI(
            broker,
            title="Device Management Broker",
            version="1.0",
            contact={
                "name": "Nikita Selivanov",
                "email": "niki_landgelo@outlook.com"
            },
        ),
        sidebar=False,
        try_it_out_path=None
    )
)
