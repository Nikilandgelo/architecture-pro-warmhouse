from fastapi import FastAPI

from .api import api_router

app = FastAPI(title="Temperature API")
app.include_router(api_router)
