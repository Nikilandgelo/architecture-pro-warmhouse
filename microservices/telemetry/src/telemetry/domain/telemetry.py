from datetime import datetime, timezone

from fastapi import HTTPException, status
from pydantic import TypeAdapter

from telemetry.adapters.repositories import TelemetryRepository
from telemetry.broker.publishers import telemetry_publisher
from telemetry.entities import Owner
from telemetry.entities import TelemetryPayload, TelemetryDBRecord, TelemetrySearchFields
from telemetry.responses import TelemetryResponse
from telemetry.security import check_device_ownership
from telemetry.settings import settings


class TelemetryService:

    @classmethod
    async def register_telemetry(cls, device_token: str, data: TelemetryPayload) -> None:
        if device_token != settings.devices_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid device token."
            )

        await TelemetryRepository.insert_telemetry(
            data=TelemetryDBRecord(
                **data.model_dump(),
                timestamp=datetime.now()
            )
        )
        await telemetry_publisher.publish(data.model_dump_json().encode())

    @classmethod
    async def get_telemetry_records(
            cls,
            owner: Owner,
            device_serial_number: str,
            limit: int = 50,
            offset: int = 0,
            timestamp: datetime | None = None,
    ) -> list[TelemetryResponse]:
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=device_serial_number,
        )

        records = await TelemetryRepository.fetch_telemetry_records(
            searching_fields=TelemetrySearchFields(
                device_serial_number=device_serial_number,
                timestamp=timestamp or datetime(1970, 1, 1, tzinfo=timezone.utc)
            ),
            limit=limit,
            offset=offset,
        )
        return TypeAdapter(list[TelemetryResponse]).validate_python(records.named_results())
