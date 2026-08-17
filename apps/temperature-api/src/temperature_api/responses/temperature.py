from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field


class TemperatureResponse(BaseModel):
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=3))).isoformat()
    )
    value: float
    sensor_id: str
    location: str
