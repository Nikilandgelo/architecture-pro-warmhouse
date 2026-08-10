from pydantic import TypeAdapter

from video_monitoring.adapters.s3 import s3_adapter
from video_monitoring.entities import Owner
from video_monitoring.responses import S3File, ListFilesResponse, PresignedUrlResponse
from video_monitoring.security import check_device_ownership


class ArchiveRecordsService:

    @classmethod
    async def get_archive_record_download_url(
            cls, owner: Owner, file_key: str
    ) -> PresignedUrlResponse:
        device_serial_number = file_key.split("/")[0]
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=device_serial_number
        )

        url = await s3_adapter.generate_presigned_url(
            client_method="get_object",
            method_params={"Key": file_key},
            expires_in=300
        )
        return PresignedUrlResponse(url=url)

    @classmethod
    async def get_device_archive_records(
            cls,
            owner: Owner,
            device_serial_number: str,
            limit: int = 10,
            next_continuation_token: str | None = None,
    ) -> ListFilesResponse:
        await check_device_ownership(
            requesting_owner=owner,
            device_serial_number=device_serial_number
        )

        response = await s3_adapter.list_objects(
            prefix=device_serial_number,
            max_keys=limit,
            continuation_token=next_continuation_token
        )
        files = TypeAdapter(list[S3File]).validate_python(response["Contents"])
        return ListFilesResponse(
            files=files,
            next_continuation_token=response.get("NextContinuationToken")
        )
