from uuid import UUID

from pydantic import BaseModel


class Owner(BaseModel):
    sub: UUID
    name: str | None
    iat: int | None
