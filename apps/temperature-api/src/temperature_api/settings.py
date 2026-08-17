from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_port: int = int(getenv("APP_PORT", 8081))
    debug: bool = bool(getenv("DEBUG", False))


settings = Settings()
