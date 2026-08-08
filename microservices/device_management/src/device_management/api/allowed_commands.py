from fastapi import APIRouter

from device_management.domain.allowed_commands import AllowedCommandsService
from device_management.responses.allowed_commands import AllowedCommandsResponse

allowed_commands_router = APIRouter()


@allowed_commands_router.get("/{type_id}")
async def get_allowed_commands(type_id: int) -> list[AllowedCommandsResponse]:
    return await AllowedCommandsService.get_allowed_commands(type_id)
