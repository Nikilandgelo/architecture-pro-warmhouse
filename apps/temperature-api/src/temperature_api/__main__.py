from uvicorn import run

from temperature_api.settings import settings


if __name__ == "__main__":
    run("temperature_api.app:app", host="0.0.0.0", port=8081, reload=settings.debug)
