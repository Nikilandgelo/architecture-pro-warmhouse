from typing import Annotated

from fastapi import APIRouter, Depends

from device_management.api.openapi import *
from device_management.domain.devices import DeviceService
from device_management.entities.device import Device, DeviceUpdate
from device_management.entities.owner import Owner
from device_management.responses.devices import DevicesResponse
from device_management.responses.generic import SuccessfulResponse
from device_management.security import get_owner_data

devices_router = APIRouter(responses=UNAUTHORIZED_RESPONSE)


@devices_router.get("/")
async def get_owner_devices(
        owner: Annotated[Owner, Depends(get_owner_data)]
) -> list[DevicesResponse]:
    return await DeviceService.get_user_devices(owner_id=owner.sub)

@devices_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses=DB_ERROR_RESPONSE
)
async def register_device(
        owner: Annotated[Owner, Depends(get_owner_data)],
        body: Device
) -> SuccessfulResponse:
    body.owner_id = owner.sub
    await DeviceService.register_device(device=body)
    return SuccessfulResponse()

@devices_router.get(
    "/{device_serial_number}",
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE}
)
async def get_specific_device(
        owner: Annotated[Owner, Depends(get_owner_data)],
        device_serial_number: str
) -> DevicesResponse:
    return await DeviceService.get_specific_device(
        owner=owner,
        device_serial_number=device_serial_number
    )

@devices_router.put(
    "/{device_serial_number}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE}
)
async def update_device(
        owner: Annotated[Owner, Depends(get_owner_data)],
        device_serial_number: str,
        body: DeviceUpdate
):
    await DeviceService.update_specific_device(
        owner=owner,
        device_serial_number=device_serial_number,
        updating_fields=body.model_dump(exclude_none=True)
    )

@devices_router.delete(
    "/{device_serial_number}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE}
)
async def deactivate_device(
        owner: Annotated[Owner, Depends(get_owner_data)],
        device_serial_number: str
):
    await DeviceService.deactivate_device(owner=owner, device_serial_number=device_serial_number)
