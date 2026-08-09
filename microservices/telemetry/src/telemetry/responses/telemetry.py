from datetime import datetime

from pydantic import BaseModel


class TelemetryResponse(BaseModel):
    device_serial_number: str
    timestamp: datetime
    device_location: str
    metrics: dict
    states: dict
