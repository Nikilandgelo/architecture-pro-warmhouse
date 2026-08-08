from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DevicesResponse(BaseModel):
    id: UUID
    created_at: datetime
    owner_id: UUID
    device_name: str
    serial_number: str
    name: str
    manufacturer: str
    installation_status: str
    activity_status: str
    location: str | None = None
    dynamic_target_value: float | None = None
    interaction_protocol: str
    measurement_unit: str | None = None

    class Config:
        from_attributes = True
