from pydantic import TypeAdapter

from device_management.adapters.repositories.devices import DevicesRepository
from device_management.enums import DeviceActivityStatuses
from device_management.loggers import service_logger
from device_management.responses.devices import DevicesResponse


class DeviceHandler:

    @classmethod
    async def change_activity_status(
            cls,
            device_serial_number: str,
            new_status: DeviceActivityStatuses
    ) -> None:
        device_old_data = TypeAdapter(DevicesResponse).validate_python(
            await DevicesRepository.get_device_by_number(
                device_serial_number=device_serial_number
            )
        )
        if new_status == device_old_data.activity_status:
            return

        await DevicesRepository.update_device(
            device_serial_number=device_serial_number,
            updating_fields={"activity_status": new_status}
        )
        service_logger.info(
            f"Taking adapter for device {device_serial_number}, protocol to "
            f"communicate is {device_old_data.interaction_protocol} and changing status "
            f"from {device_old_data.activity_status} to {new_status}."
        )
        ...

    @classmethod
    async def change_target_value(cls, device_serial_number: str, new_value: float) -> None:
        device_old_data = TypeAdapter(DevicesResponse).validate_python(
            await DevicesRepository.get_device_by_number(
                device_serial_number=device_serial_number
            )
        )
        if (
                device_old_data.dynamic_target_value is None or
                new_value == device_old_data.dynamic_target_value
        ):
            return

        await DevicesRepository.update_device(
            device_serial_number=device_serial_number,
            updating_fields={"dynamic_target_value": new_value}
        )
        service_logger.info(
            f"Taking adapter for device {device_serial_number}, protocol to "
            f"communicate is {device_old_data.interaction_protocol} and changing value "
            f"from {device_old_data.dynamic_target_value} to {new_value}."
        )
        ...
