from pydantic import BaseModel


class DeviceTypesResponse(BaseModel):
    id: int
    name: str
    manufacturer: str

    class Config:
        from_attributes = True
