import uuid
from datetime import datetime

from sqlalchemy import (
    func, String, Text, Identity, Boolean, ForeignKey, Double, UUID, DateTime, Index, text,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import MetaData


class Base(DeclarativeBase):
    metadata = MetaData(schema="public")


class DeviceTypes(Base):
    __tablename__ = "device_types"

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
    name: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        unique=True,
        index=True,
        comment="Unique human-readable name of the device type."
    )
    manufacturer: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )
    interaction_protocol: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Protocol used to interact with devices of this type, for example MQTT, HTTP, etc."
    )
    measurement_unit: Mapped[str | None] = mapped_column(
        String(),
        comment="Default measurement unit used by devices of this type."
    )
    has_dynamic_values: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
        default=False,
        comment="Indicates whether devices of this type support dynamic target values."
    )


class Devices(Base):
    __tablename__ = "devices"
    __table_args__ = (
        Index(
            "devices_serial_number_active_uidx",
            "serial_number",
            unique=True,
            postgresql_where=text("installation_status = 'active'"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
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
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(),
        nullable=False,
        index=True,
        comment="UUID identifier of the user that owns the device."
    )
    name: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        comment="Human-readable name of the device."
    )
    serial_number: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        unique=True,
        index=True,
        comment="Unique serial number assigned to the physical device."
    )
    type_id: Mapped[int] = mapped_column(
        ForeignKey("device_types.id"),
        nullable=False,
        index=True,
        comment="Reference to the device type in the device_types table."
    )
    installation_status: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="active",
        comment="Current installation status of the device, for example active, inactive, etc."
    )
    activity_status: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="off",
        comment="Current operational activity status of the device, for example on, off, etc."
    )
    location: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment="Current location of the device."
    )
    dynamic_target_value: Mapped[float | None] = mapped_column(
        Double(),
        comment=(
            "Optional dynamic target value used by devices that support configurable target "
            "values."
        )
    )
    extra_data: Mapped[dict | None] = mapped_column("metadata", JSONB)


class AllowedCommands(Base):
    __tablename__ = "allowed_commands"
    __table_args__ = (
        UniqueConstraint("type_id", "command", name="allowed_commands_type_id_command_key"),
    )

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
        comment="Soft-delete flag indicating whether the command is considered deleted."
    )
    type_id: Mapped[int] = mapped_column(
        ForeignKey("device_types.id"),
        nullable=False,
        index=True,
        comment="Reference to the device type for which this command is allowed."
    )
    command: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment="Unique command that is allowed and can be proceed for a specific device type."
    )
    command_extra_data: Mapped[dict | None] = mapped_column(JSONB)
