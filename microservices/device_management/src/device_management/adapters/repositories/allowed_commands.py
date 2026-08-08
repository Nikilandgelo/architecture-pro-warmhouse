from sqlalchemy import select, Sequence, RowMapping

from device_management.db import session_factory, AllowedCommands


class AllowedCommandsRepository:

    @staticmethod
    async def get_type_allowed_commands(type_id: int) -> Sequence[RowMapping]:
        async with session_factory() as session:
            stmt = (
                select(
                    AllowedCommands.id,
                    AllowedCommands.created_at,
                    AllowedCommands.command,
                    AllowedCommands.type_id
                )
                .where(
                    AllowedCommands.type_id == type_id,
                    AllowedCommands.is_deleted.is_(False)
                )
            )
            result = await session.execute(stmt)
            return result.mappings().all()
