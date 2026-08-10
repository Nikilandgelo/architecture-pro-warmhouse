from datetime import datetime

from pydantic import BaseModel, Field


class S3File(BaseModel):
    key: str = Field(alias="Key")
    last_modified: datetime = Field(alias="LastModified")
    size: int = Field(alias="Size")


class ListFilesResponse(BaseModel):
    files: list[S3File]
    next_continuation_token: str | None = None


class PresignedUrlResponse(BaseModel):
    url: str
