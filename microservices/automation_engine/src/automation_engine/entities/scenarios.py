from uuid import UUID

from pydantic import BaseModel


class Conditions(BaseModel):
    metrics: dict[str, float] | None = None
    states: dict[str, str] | None = None

    class Config:
        extra = "forbid"


class Scenario(BaseModel):
    name: str
    trigger_serial_number: str
    conditions: Conditions | None = None
    owner_id: UUID | None = None


class ScenarioUpdate(BaseModel):
    is_deleted: bool | None = None
    is_enabled: bool | None = None
    name: str | None = None
    trigger_serial_number: str | None = None
    conditions: Conditions | None = None


class ScenarioAction(BaseModel):
    target_serial_number: str
    action_command: str
    action_command_extra_data: dict | None = None


class ScenarioActionUpdate(BaseModel):
    is_deleted: bool | None = None
    target_serial_number: str | None = None
    action_command: str | None = None
    action_command_extra_data: dict | None = None
