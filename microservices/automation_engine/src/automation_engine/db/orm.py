import uuid
from datetime import datetime

from sqlalchemy import (
    func, String, Text, Identity, Boolean, ForeignKey, UUID, DateTime
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import MetaData


class Base(DeclarativeBase):
    metadata = MetaData(schema="public")


class Scenarios(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False,
        comment="Soft-delete flag indicating whether the scenario is considered deleted."
    )
    is_enabled: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=True,
        comment="Indicates whether the scenario is currently active and should be evaluated."
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
        index=True,
        comment="UUID identifier of the user that owns the scenario."
    )
    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Human-readable name of the scenario."
    )
    trigger_serial_number: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        index=True,
        comment="Serial number of the device whose event triggers this scenario."
    )
    conditions: Mapped[dict | None] = mapped_column(
        JSONB(),
        comment="Optional conditions that must be met for the scenario to trigger."
    )


class ScenariosActions(Base):
    __tablename__ = "scenarios_actions"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False,
        comment="Soft-delete flag indicating whether the action is considered deleted."
    )
    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id"),
        nullable=False,
        index=True,
        comment="Reference to the scenario this action belongs to."
    )
    target_serial_number: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment="Serial number of the device this action is applied to."
    )
    action_command: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment="Command to be executed on the target device when the scenario triggers."
    )
    action_command_extra_data: Mapped[dict | None] = mapped_column(JSONB)
