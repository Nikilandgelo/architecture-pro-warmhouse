from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(default=False)
    jwt_secret_key: str = Field(validation_alias="JWT_HS_256_SECRET_KEY")

    app_port: int

    nats_url: str
    nats_commands_stream: str
    nats_events_stream: str
    nats_key_value: str
    max_tasks_per_worker: int

    clickhouse_username: str = Field(validation_alias="CLICK_USER")
    clickhouse_password: str = Field(validation_alias="CLICK_PASSWORD")
    clickhouse_host: str = Field(validation_alias="CLICK_HOSTNAME")
    clickhouse_port: int = Field(validation_alias="CLICK_PORT")
    clickhouse_database: str = Field(validation_alias="CLICK_DB_NAME")

    devices_token: str

settings = Settings()
