from pydantic import TypeAdapter

from device_management.adapters.repositories.device_types import DeviceTypesRepository
from device_management.responses.device_types import DeviceTypesResponse


class DeviceTypesService:

    @classmethod
    async def get_device_types(
            cls,
            limit: int,
            last_device_type_id: int | None = None
    ) -> list[DeviceTypesResponse]:
        device_types = await DeviceTypesRepository.get_device_types(
            limit=limit,
            last_device_type_id=last_device_type_id
        )
        return TypeAdapter(list[DeviceTypesResponse]).validate_python(device_types)
