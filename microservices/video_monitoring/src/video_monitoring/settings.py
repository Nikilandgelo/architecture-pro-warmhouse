from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(default=False)
    app_port: int
    jwt_secret_key: str = Field(validation_alias="JWT_HS_256_SECRET_KEY")


settings = Settings()
