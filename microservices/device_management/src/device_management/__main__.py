from uvicorn import run
from .settings import settings


if __name__ == "__main__":
    run("device_management.app:app", host="0.0.0.0", port=settings.app_port, reload=settings.debug)
