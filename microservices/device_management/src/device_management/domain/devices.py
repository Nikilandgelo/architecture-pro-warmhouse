from uuid import UUID

from fastapi import HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy.exc import DBAPIError

from device_management.adapters.nats import devices_kv_store
from device_management.adapters.repositories.device_types import DeviceTypesRepository
from device_management.adapters.repositories.devices import DevicesRepository
from device_management.entities.device import Device
from device_management.entities.owner import Owner
from device_management.enums import DeviceInstallationStatuses, DeviceActivityStatuses
from device_management.handlers import DeviceHandler
from device_management.responses.devices import DevicesResponse
from device_management.security import check_device_ownership


class DeviceService:

    @classmethod
    async def _update_postprocess(
            cls,
            device_serial_number: str,
            new_activity_status: DeviceActivityStatuses | None,
            new_value: float | None
    ) -> None:
        if new_activity_status is not None:
            await DeviceHandler.change_activity_status(
                device_serial_number=device_serial_number,
                new_status=new_activity_status
            )

        if new_value is not None:
            await DeviceHandler.change_target_value(
                device_serial_number=device_serial_number,
                new_value=float(new_value)
            )

    @classmethod
    async def get_user_devices(cls, owner_id: UUID) -> list[DevicesResponse]:
        devices = await DevicesRepository.get_owner_devices(owner_id=owner_id)
        return TypeAdapter(list[DevicesResponse]).validate_python(devices)

    @classmethod
    async def register_device(cls, device: Device) -> None:
        dynamic_target_value = None
        device_type = await DeviceTypesRepository.get_type_by_id(type_id=device.type_id)
        if not device_type:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Device type not found"
            )

        if device_type.get("has_dynamic_values", False):
            dynamic_target_value = 0.0

        try:
            await DevicesRepository.create_device(
                device_data=device,
                dynamic_target_value=dynamic_target_value
            )
            await devices_kv_store.put(key=device.serial_number, value=str(device.owner_id))
        except DBAPIError as error:
            detail = getattr(error.orig.__cause__, "detail", "Something went wrong")
            raise HTTPException(status.HTTP_409_CONFLICT, detail=detail)

    @classmethod
    async def get_specific_device(cls, owner: Owner, device_serial_number: str) -> DevicesResponse:
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=device_serial_number
        )

        device = await DevicesRepository.get_device_by_number(
            device_serial_number=device_serial_number
        )
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        return TypeAdapter(DevicesResponse).validate_python(device)

    @classmethod
    async def update_specific_device(
            cls,
            owner: Owner,
            device_serial_number: str,
            updating_fields: dict
    ) -> None:
        new_activity_status: DeviceActivityStatuses | None = updating_fields.pop(
            "activity_status", None
        )
        new_value: float | None = updating_fields.pop("dynamic_target_value", None)

        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=device_serial_number
        )
        if len(updating_fields) > 0:
            await DevicesRepository.update_device(
                device_serial_number=device_serial_number,
                updating_fields=updating_fields
            )

        await cls._update_postprocess(
            device_serial_number=device_serial_number,
            new_activity_status=new_activity_status,
            new_value=new_value
        )

    @classmethod
    async def deactivate_device(cls, owner: Owner, device_serial_number: str) -> None:
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=device_serial_number
        )
        await DevicesRepository.update_device(
            device_serial_number=device_serial_number,
            updating_fields={"installation_status": DeviceInstallationStatuses.Inactive}
        )
        await devices_kv_store.delete(key=device_serial_number)
