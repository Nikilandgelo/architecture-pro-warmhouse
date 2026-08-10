from uuid import UUID

from sqlalchemy import select, Sequence, RowMapping, func, update

from automation_engine.db import session_factory, Scenarios, ScenariosActions


class ScenariosRepository:

    @staticmethod
    async def get_owner_scenarios(owner_id: UUID) -> Sequence[RowMapping]:
        async with session_factory() as session:
            stmt = (
                select(
                    Scenarios.id,
                    Scenarios.created_at,
                    Scenarios.is_enabled,
                    Scenarios.owner_id,
                    Scenarios.name,
                    Scenarios.trigger_serial_number,
                    Scenarios.conditions
                )
                .where(Scenarios.owner_id == owner_id, Scenarios.is_deleted.is_(False))
                .order_by(Scenarios.created_at.desc())
            )
            result = await session.execute(stmt)
            return result.mappings().all()

    @staticmethod
    async def create_scenario(data: dict) -> None:
        async with session_factory() as session:
            session.add(Scenarios(**data))
            await session.commit()

    @staticmethod
    async def get_specific_scenario(scenario_id: int, owner_id: UUID) -> RowMapping | None:
        async with session_factory() as session:
            stmt = (
                select(
                    Scenarios.id,
                    Scenarios.created_at,
                    Scenarios.is_enabled,
                    Scenarios.owner_id,
                    Scenarios.name,
                    Scenarios.trigger_serial_number,
                    Scenarios.conditions,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id", ScenariosActions.id,
                            "target_serial_number", ScenariosActions.target_serial_number,
                            "action_command", ScenariosActions.action_command,
                            "action_command_extra_data", ScenariosActions.action_command_extra_data
                        )
                    ).filter(ScenariosActions.id.is_not(None)).label("actions")
                )
                .where(
                    Scenarios.id == scenario_id,
                    Scenarios.owner_id == owner_id,
                    Scenarios.is_deleted.is_(False)
                )
                .outerjoin(
                    ScenariosActions,
                    (
                        (ScenariosActions.scenario_id == Scenarios.id) &
                        (ScenariosActions.is_deleted.is_(False))
                    )
                )
                .group_by(Scenarios.id)
            )
            result = await session.execute(stmt)
            return result.mappings().first()

    @staticmethod
    async def update_specific_scenario(scenario_id: int, owner_id: UUID, data: dict) -> None:
        async with session_factory() as session:
            stmt = (
                update(Scenarios)
                .where(
                    Scenarios.id == scenario_id,
                    Scenarios.owner_id == owner_id,
                    Scenarios.is_deleted.is_(False)
                )
                .values(**data)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def create_scenarios_action(data: dict) -> None:
        async with session_factory() as session:
            session.add(ScenariosActions(**data))
            await session.commit()

    @staticmethod
    async def fetch_scenarios_action(scenarios_action_id: int, owner_id: UUID) -> RowMapping | None:
        async with session_factory() as session:
            stmt = (
                select(
                    ScenariosActions.id,
                    ScenariosActions.created_at,
                    ScenariosActions.scenario_id,
                    ScenariosActions.target_serial_number,
                    ScenariosActions.action_command,
                    ScenariosActions.action_command_extra_data,
                )
                .join(Scenarios, ScenariosActions.scenario_id == Scenarios.id)
                .where(
                    ScenariosActions.id == scenarios_action_id,
                    ScenariosActions.is_deleted.is_(False),
                    Scenarios.owner_id == owner_id,
                    Scenarios.is_deleted.is_(False)
                )
            )
            result = await session.execute(stmt)
            return result.mappings().first()

    @staticmethod
    async def update_scenarios_action(scenarios_action_id: int, data: dict) -> None:
        async with session_factory() as session:
            stmt = (
                update(ScenariosActions)
                .where(ScenariosActions.id == scenarios_action_id)
                .values(**data)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def find_scenarios_by_device(trigger_serial_number: str) -> Sequence[RowMapping]:
        async with session_factory() as session:
            stmt = (
                select(
                    Scenarios.id,
                    Scenarios.is_enabled,
                    Scenarios.owner_id,
                    Scenarios.trigger_serial_number,
                    Scenarios.conditions,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id", ScenariosActions.id,
                            "target_serial_number", ScenariosActions.target_serial_number,
                            "action_command", ScenariosActions.action_command,
                            "action_command_extra_data", ScenariosActions.action_command_extra_data
                        )
                    ).filter(ScenariosActions.id.is_not(None)).label("actions")
                )
                .where(
                    Scenarios.trigger_serial_number == trigger_serial_number,
                    Scenarios.is_deleted.is_(False),
                    Scenarios.is_enabled.is_(True),
                )
                .outerjoin(
                    ScenariosActions,
                    (
                            (ScenariosActions.scenario_id == Scenarios.id) &
                            (ScenariosActions.is_deleted.is_(False))
                    )
                )
                .group_by(Scenarios.id)
            )
            result = await session.execute(stmt)
            return result.mappings().all()
