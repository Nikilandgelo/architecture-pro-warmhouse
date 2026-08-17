from pydantic import BaseModel, Field


class TelemetryPayload(BaseModel):
    device_serial_number: str
    device_location: str
    metrics: dict[str, float] = Field(default_factory=dict)
    states: dict[str, str] = Field(default_factory=dict)
