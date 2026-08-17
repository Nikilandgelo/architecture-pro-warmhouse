from typing import Annotated

from fastapi import APIRouter, Depends, Query

from video_monitoring.api.openapi import (
    UNAUTHORIZED_RESPONSE,
    DEVICE_NOT_FOUND_RESPONSE,
    DEVICE_DIFFERENT_OWNER_RESPONSE
)
from video_monitoring.domain import ArchiveRecordsService
from video_monitoring.entities import Owner
from video_monitoring.responses import ListFilesResponse, PresignedUrlResponse
from video_monitoring.security import get_owner_data

archive_records_router = APIRouter(responses=UNAUTHORIZED_RESPONSE)


@archive_records_router.get(
    "/download",
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE},
)
async def get_archive_record_download_url(
        owner: Annotated[Owner, Depends(get_owner_data)],
        file_key: Annotated[str, Query(
            description="File key from S3, which can contain trailing slashes, etc."
        )]
) -> PresignedUrlResponse:
    return await ArchiveRecordsService.get_archive_record_download_url(
        owner=owner, file_key=file_key
    )


@archive_records_router.get(
    "/{device_serial_number}",
    responses={**DEVICE_NOT_FOUND_RESPONSE, **DEVICE_DIFFERENT_OWNER_RESPONSE},
)
async def get_device_archive_records(
        owner: Annotated[Owner, Depends(get_owner_data)],
        device_serial_number: str,
        limit: Annotated[int, Query(gt=0, le=50)] = 10,
        next_continuation_token: str | None = None,
) -> ListFilesResponse:
    return await ArchiveRecordsService.get_device_archive_records(
        owner=owner,
        device_serial_number=device_serial_number,
        limit=limit,
        next_continuation_token=next_continuation_token
    )
