from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Header, status, Depends, Query

from telemetry.api.openapi import (
    WRONG_TOKEN_RESPONSE,
    DEVICE_NOT_FOUND_RESPONSE,
    DEVICE_DIFFERENT_OWNER_RESPONSE,
    UNAUTHORIZED_RESPONSE
)
from telemetry.domain.telemetry import TelemetryService
from telemetry.entities import TelemetryPayload, Owner
from telemetry.responses import SuccessfulResponse
from telemetry.responses import TelemetryResponse
from telemetry.security import get_owner_data

telemetry_router = APIRouter()


@telemetry_router.post(
    "/",
    responses=WRONG_TOKEN_RESPONSE,
    status_code=status.HTTP_201_CREATED
)
async def register_device_telemetry(
        device_token: Annotated[
            str,
            Header(
                alias="Device-Token",
                description=(
                        "MUST be unique per device in real world, but for mocking light purposes "
                        "it's just using static 1 token from .env for ALL devices!"
                )
            )
        ],
        body: TelemetryPayload,
) -> SuccessfulResponse:
    await TelemetryService.register_telemetry(device_token=device_token, data=body)
    return SuccessfulResponse()

@telemetry_router.get(
    "/{device_serial_number}",
    responses={
        **UNAUTHORIZED_RESPONSE,
        **DEVICE_NOT_FOUND_RESPONSE,
        **DEVICE_DIFFERENT_OWNER_RESPONSE
    },
)
async def get_device_telemetry(
        owner: Annotated[Owner, Depends(get_owner_data)],
        device_serial_number: str,
        limit: int = Query(default=50, ge=1, le=500),
        offset: int = Query(default=0, ge=0),
        timestamp: datetime | None = None,
) -> list[TelemetryResponse]:
    return await TelemetryService.get_telemetry_records(
        owner=owner,
        device_serial_number=device_serial_number,
        limit=limit,
        offset=offset,
        timestamp=timestamp
    )
