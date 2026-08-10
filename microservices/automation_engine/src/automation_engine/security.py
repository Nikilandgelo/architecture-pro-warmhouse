import jwt
from automation_engine.adapters.nats import devices_kv_store
from automation_engine.entities.owner import Owner
from fastapi import status, HTTPException
from jwt.exceptions import PyJWTError
from nats.js.errors import KeyNotFoundError
from starlette.requests import Request

from automation_engine.loggers import service_logger
from automation_engine.settings import settings


def get_owner_data(request: Request) -> Owner:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials is invalid."
        )

    token = auth_header.split("Bearer ")[1]
    try:
        jwt_data = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        return Owner(**jwt_data)
    except PyJWTError as error:
        service_logger.exception(str(error))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials is invalid."
        )


async def check_device_ownership(requesting_owner: Owner, device_serial_number: str) -> None:
    try:
        kv_entry = await devices_kv_store.get(key=device_serial_number)
    except KeyNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    if str(requesting_owner.sub) != kv_entry.value.decode():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
