from contextlib import asynccontextmanager

from fastapi import FastAPI

from video_monitoring.adapters.nats import devices_kv_store
from video_monitoring.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await devices_kv_store.startup()
    yield
    await devices_kv_store.shutdown()


app = FastAPI(
    title="Video Monitoring API",
    version="1.0",
    contact={
        "name": "Nikita Selivanov",
        "email": "niki_landgelo@outlook.com"
    },
    lifespan=lifespan
)
app.include_router(api_router)
