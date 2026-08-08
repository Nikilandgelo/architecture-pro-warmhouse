from sqlalchemy import select, Sequence, RowMapping

from device_management.db import session_factory, DeviceTypes


class DeviceTypesRepository:

    @staticmethod
    async def get_device_types(
            limit: int,
            last_device_type_id: int | None = None
    ) -> Sequence[RowMapping]:
        async with session_factory() as session:
            stmt = (
                select(DeviceTypes.id, DeviceTypes.name, DeviceTypes.manufacturer)
                .order_by(DeviceTypes.id)
                .limit(limit)
            )
            if last_device_type_id:
                stmt = stmt.where(DeviceTypes.id > last_device_type_id)

            result = await session.execute(stmt)
            return result.mappings().all()

    @staticmethod
    async def get_type_by_id(type_id: int) -> RowMapping | None:
        async with session_factory() as session:
            stmt = (
                select(
                    DeviceTypes.id,
                    DeviceTypes.name,
                    DeviceTypes.manufacturer,
                    DeviceTypes.interaction_protocol,
                    DeviceTypes.measurement_unit,
                    DeviceTypes.has_dynamic_values
                )
                .where(DeviceTypes.id == type_id)
            )

            result = await session.execute(stmt)
            return result.mappings().first()
