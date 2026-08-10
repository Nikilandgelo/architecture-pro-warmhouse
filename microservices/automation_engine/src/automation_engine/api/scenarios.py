from typing import Annotated

from fastapi import APIRouter, Depends, status

from automation_engine.api.openapi import (
    UNAUTHORIZED_RESPONSE,
    DEVICE_NOT_FOUND_RESPONSE,
    DEVICE_DIFFERENT_OWNER_RESPONSE,
    SCENARIO_NOT_FOUND_RESPONSE,
    DEVICE_SCENARIO_NOT_FOUND_RESPONSE
)
from automation_engine.domain.scenarios import ScenariosService
from automation_engine.entities import (
    Owner,
    Scenario,
    ScenarioUpdate,
    ScenarioAction,
    ScenarioActionUpdate
)
from automation_engine.responses import (
    SuccessfulResponse,
    ScenarioResponse,
    DetailedScenarioResponse
)
from automation_engine.security import get_owner_data

scenarios_router = APIRouter(responses=UNAUTHORIZED_RESPONSE)

@scenarios_router.get("/")
async def get_owner_scenarios(
        owner: Annotated[Owner, Depends(get_owner_data)]
) -> list[ScenarioResponse]:
    return await ScenariosService.get_owner_scenarios(owner=owner)

@scenarios_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE},
)
async def create_scenario(
        owner: Annotated[Owner, Depends(get_owner_data)],
        body: Scenario
) -> SuccessfulResponse:
    await ScenariosService.create_scenario(owner=owner, data=body)
    return SuccessfulResponse()

@scenarios_router.get("/{scenario_id}", responses=SCENARIO_NOT_FOUND_RESPONSE)
async def get_specific_scenario(
        scenario_id: int,
        owner: Annotated[Owner, Depends(get_owner_data)]
) -> DetailedScenarioResponse:
    return await ScenariosService.get_specific_scenario(scenario_id=scenario_id, owner=owner)

@scenarios_router.put(
    "/{scenario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE},
)
async def update_scenario(
        scenario_id: int,
        owner: Annotated[Owner, Depends(get_owner_data)],
        body: ScenarioUpdate
):
    await ScenariosService.update_specific_scenario(
        scenario_id=scenario_id,
        owner=owner, data=body
    )

@scenarios_router.post(
    "/{scenario_id}/assign-action",
    status_code=status.HTTP_201_CREATED,
    responses={**DEVICE_SCENARIO_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE}
)
async def assign_action(
        scenario_id: int,
        owner: Annotated[Owner, Depends(get_owner_data)],
        body: ScenarioAction
) -> SuccessfulResponse:
    await ScenariosService.assign_action(scenario_id=scenario_id, owner=owner, data=body)
    return SuccessfulResponse()

@scenarios_router.put(
    "/actions/{scenarios_action_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**DEVICE_SCENARIO_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE})
async def update_scenario_action(
        scenarios_action_id: int,
        owner: Annotated[Owner, Depends(get_owner_data)],
        body: ScenarioActionUpdate
):
    await ScenariosService.update_scenario_action(
        scenario_action_id=scenarios_action_id, owner=owner, data=body
    )
