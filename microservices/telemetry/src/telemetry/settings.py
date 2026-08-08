from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(default=False)
    app_port: int
    jwt_secret_key: str = Field(validation_alias="JWT_HS_256_SECRET_KEY")

    nats_url: str
    nats_commands_stream: str
    nats_events_stream: str
    nats_key_value: str
    max_tasks_per_worker: int


settings = Settings()
