from uvicorn import run

from .settings import settings

if __name__ == "__main__":
    run("automation_engine.app:app", host="0.0.0.0", port=settings.app_port, reload=settings.debug)
