from pydantic import BaseModel


class ActivityStatusPayload(BaseModel):
    device_serial_number: str
    activity_status: str


class DynamicValuePayload(BaseModel):
    device_serial_number: str
    new_value: float
