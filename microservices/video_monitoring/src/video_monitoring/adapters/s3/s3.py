from aioboto3 import Session

from video_monitoring.settings import settings


class S3Adapter(Session):

    def __init__(self):
        super().__init__(
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
        )

    async def list_objects(
            self,
            prefix: str | None = None,
            max_keys: int = 10,
            continuation_token: str | None = None
    ) -> dict:
        params = {"Bucket": settings.s3_bucket}
        if prefix is not None:
            params["Prefix"] = f"{prefix}/"

        if max_keys:
            params["MaxKeys"] = max_keys

        if continuation_token is not None:
            params["ContinuationToken"] = continuation_token
        else:
            params["StartAfter"] = f"{prefix}/"  # fix "folder" zero file in a response

        async with self.client("s3", endpoint_url=settings.s3_endpoint_url) as client:
            response = await client.list_objects_v2(**params)

        return response

    async def generate_presigned_url(
            self,
            client_method: str,
            method_params: dict,
            expires_in: int = 3600
    ) -> str:
        method_params["Bucket"] = settings.s3_bucket
        params = {
            "ClientMethod": client_method,
            "Params": method_params,
            "ExpiresIn": expires_in
        }

        async with self.client("s3", endpoint_url=settings.s3_endpoint_url) as client:
            response = await client.generate_presigned_url(**params)
            return response

s3_adapter = S3Adapter()
