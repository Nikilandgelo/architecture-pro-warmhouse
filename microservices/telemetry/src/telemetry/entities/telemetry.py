from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, Field


class TelemetryPayload(BaseModel):
    device_serial_number: str
    device_location: str
    metrics: dict[str, float] = Field(default_factory=dict)
    states: dict[str, str] = Field(default_factory=dict)


@dataclass(slots=True)
class TelemetryDBRecord:
    __tablename__: ClassVar[str] = "telemetry_record"

    device_serial_number: str
    timestamp: datetime
    device_location: str
    metrics: dict[str, float]
    states: dict[str, str]


class TelemetrySearchFields(BaseModel):
    device_serial_number: str
    timestamp: datetime
