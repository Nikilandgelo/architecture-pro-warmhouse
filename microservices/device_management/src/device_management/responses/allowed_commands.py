from datetime import datetime

from pydantic import BaseModel


class AllowedCommandsResponse(BaseModel):
    id: int
    created_at: datetime
    command: str
    type_id: int
