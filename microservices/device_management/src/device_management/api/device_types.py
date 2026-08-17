from fastapi import APIRouter

from device_management.domain.device_types import DeviceTypesService
from device_management.responses.device_types import DeviceTypesResponse

device_types_router = APIRouter()


@device_types_router.get("/")
async def get_possible_devices(
        limit: int = 20,
        last_device_type_id: int | None = None
) -> list[DeviceTypesResponse]:
    return await DeviceTypesService.get_device_types(
        limit=limit,
        last_device_type_id=last_device_type_id
    )
