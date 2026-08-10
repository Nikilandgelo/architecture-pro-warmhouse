from fastapi import HTTPException, status
from pydantic import TypeAdapter

from automation_engine.adapters.repositories import ScenariosRepository
from automation_engine.entities import (
    Scenario,
    Owner,
    ScenarioUpdate,
    ScenarioAction,
    ScenarioActionUpdate
)
from automation_engine.responses import ScenarioResponse, DetailedScenarioResponse
from automation_engine.security import check_device_ownership


class ScenariosService:

    @classmethod
    async def get_owner_scenarios(cls, owner: Owner) -> list[ScenarioResponse]:
        scenarios = await ScenariosRepository.get_owner_scenarios(owner_id=owner.sub)
        return TypeAdapter(list[ScenarioResponse]).validate_python(scenarios)

    @classmethod
    async def create_scenario(cls, owner: Owner, data: Scenario) -> None:
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=data.trigger_serial_number
        )
        data.owner_id = owner.sub
        await ScenariosRepository.create_scenario(data=data.model_dump())

    @classmethod
    async def get_specific_scenario(
            cls, scenario_id: int, owner: Owner
    ) -> DetailedScenarioResponse:
        scenario = await ScenariosRepository.get_specific_scenario(
            scenario_id=scenario_id, owner_id=owner.sub
        )
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        return TypeAdapter(DetailedScenarioResponse).validate_python(scenario)

    @classmethod
    async def update_specific_scenario(
            cls, scenario_id: int, owner: Owner, data: ScenarioUpdate
    ) -> None:
        updating_fields = data.model_dump(exclude_none=True)
        if len(updating_fields) == 0:
            return

        if new_trigger_device := updating_fields.get("trigger_serial_number"):
            await check_device_ownership(
                requesting_owner=owner,
                device_serial_number=new_trigger_device
            )

        await ScenariosRepository.update_specific_scenario(
            scenario_id=scenario_id, owner_id=owner.sub, data=updating_fields
        )

    @classmethod
    async def assign_action(
            cls, scenario_id: int, owner: Owner, data: ScenarioAction
    ) -> None:
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=data.target_serial_number
        )
        scenario = await ScenariosRepository.get_specific_scenario(
            scenario_id=scenario_id, owner_id=owner.sub
        )
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        await ScenariosRepository.create_scenarios_action(
            data.model_dump(exclude_none=True) | {"scenario_id": scenario_id}
        )

    @classmethod
    async def update_scenario_action(
            cls, scenario_action_id: int, owner: Owner, data: ScenarioActionUpdate
    ) -> None:
        updating_fields = data.model_dump(exclude_none=True)
        if len(updating_fields) == 0:
            return

        if new_target_device := updating_fields.get("target_serial_number"):
            await check_device_ownership(
                requesting_owner=owner,
                device_serial_number=new_target_device
            )

        scenario_action = await ScenariosRepository.fetch_scenarios_action(
            scenarios_action_id=scenario_action_id,
            owner_id=owner.sub
        )
        if not scenario_action:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        await ScenariosRepository.update_scenarios_action(
            scenarios_action_id=scenario_action_id, data=updating_fields
        )
