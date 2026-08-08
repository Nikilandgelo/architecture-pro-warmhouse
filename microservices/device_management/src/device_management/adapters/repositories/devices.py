from uuid import UUID

from sqlalchemy import select, Sequence, RowMapping, update

from device_management.db import session_factory, Devices, DeviceTypes
from device_management.entities.device import Device
from device_management.enums import DeviceInstallationStatuses


class DevicesRepository:

    @staticmethod
    async def get_owner_devices(owner_id: UUID | None = None) -> Sequence[RowMapping]:
        async with session_factory() as session:
            stmt = (
                select(
                    Devices.id,
                    Devices.created_at,
                    Devices.owner_id,
                    Devices.name.label("device_name"),
                    Devices.serial_number,
                    DeviceTypes.name,
                    DeviceTypes.manufacturer,
                    Devices.installation_status,
                    Devices.activity_status,
                    Devices.location,
                    Devices.dynamic_target_value,
                    DeviceTypes.interaction_protocol,
                    DeviceTypes.measurement_unit
                )
                .join(DeviceTypes, Devices.type_id == DeviceTypes.id)
                .where(Devices.installation_status != DeviceInstallationStatuses.Inactive)
            )
            if owner_id is not None:
                stmt = stmt.where(Devices.owner_id == owner_id)

            result = await session.execute(stmt)
            return result.mappings().all()

    @staticmethod
    async def create_device(device_data: Device, dynamic_target_value: float | None = None) -> None:
        async with session_factory() as session:
            session.add(
                Devices(**device_data.model_dump(), dynamic_target_value=dynamic_target_value)
            )
            await session.commit()

    @staticmethod
    async def get_device_by_number(device_serial_number: str) -> RowMapping | None:
        async with session_factory() as session:
            stmt = (
                select(
                    Devices.id,
                    Devices.created_at,
                    Devices.owner_id,
                    Devices.name.label("device_name"),
                    Devices.serial_number,
                    DeviceTypes.name,
                    DeviceTypes.manufacturer,
                    Devices.installation_status,
                    Devices.activity_status,
                    Devices.location,
                    Devices.dynamic_target_value,
                    DeviceTypes.interaction_protocol,
                    DeviceTypes.measurement_unit
                )
                .join(DeviceTypes, Devices.type_id == DeviceTypes.id)
                .where(
                    Devices.serial_number == device_serial_number,
                    Devices.installation_status != DeviceInstallationStatuses.Inactive
                )
            )
            result = await session.execute(stmt)
            return result.mappings().first()

    @staticmethod
    async def update_device(device_serial_number: str, updating_fields: dict) -> None:
        async with session_factory() as session:
            stmt = (
                update(Devices)
                .values(**updating_fields)
                .where(
                    Devices.serial_number == device_serial_number,
                    Devices.installation_status != DeviceInstallationStatuses.Inactive
                )
            )
            await session.execute(stmt)
            await session.commit()
