from datetime import datetime

from pydantic import BaseModel


class AllowedCommandsResponse(BaseModel):
    id: int
    created_at: datetime
    type_id: int
    command: str
    command_extra_data: dict
