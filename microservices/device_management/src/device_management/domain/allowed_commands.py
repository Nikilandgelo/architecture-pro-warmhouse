from pydantic import TypeAdapter

from device_management.adapters.repositories.allowed_commands import AllowedCommandsRepository
from device_management.responses.allowed_commands import AllowedCommandsResponse


class AllowedCommandsService:

    @classmethod
    async def get_allowed_commands(cls, type_id: int) -> list[AllowedCommandsResponse]:
        commands = await AllowedCommandsRepository.get_type_allowed_commands(type_id=type_id)
        return TypeAdapter(list[AllowedCommandsResponse]).validate_python(commands)
