from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from automation_engine.entities import Conditions


class ScenarioResponse(BaseModel):
    id: int
    created_at: datetime
    is_enabled: bool
    owner_id: UUID
    name: str
    trigger_serial_number: str
    conditions: Conditions


class ScenarioActionsResponse(BaseModel):
    id: int
    target_serial_number: str
    action_command: str
    action_command_extra_data: dict


class DetailedScenarioResponse(ScenarioResponse):
    actions: list[ScenarioActionsResponse] | None = None

    @field_validator("actions")
    @classmethod
    def validate_actions(
            cls, value: list[ScenarioActionsResponse] | None
    ) -> list[ScenarioActionsResponse]:
        if value is None:
            return []

        return value
