from uuid import UUID

from pydantic import BaseModel

from device_management.enums import DeviceActivityStatuses


class Device(BaseModel):
    name: str
    serial_number: str
    type_id: int
    location: str
    owner_id: UUID | None = None
    metadata: dict | None = None


class DeviceUpdate(BaseModel):
    name: str | None = None
    activity_status: DeviceActivityStatuses | None = None
    location: str | None = None
    dynamic_target_value: float | None = None
    metadata: dict | None = None


class ActivityStatusPayload(BaseModel):
    device_serial_number: str
    activity_status: DeviceActivityStatuses


class DynamicTargetValuePayload(BaseModel):
    device_serial_number: str
    new_value: float
