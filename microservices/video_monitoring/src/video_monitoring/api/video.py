import asyncio
import secrets
from typing import Annotated

from fastapi import APIRouter, WebSocket, Depends, status
from starlette.websockets import WebSocketDisconnect

from video_monitoring.entities import Owner
from video_monitoring.loggers import service_logger
from video_monitoring.security import check_device_ownership_ws
from video_monitoring.security import get_owner_data_ws

video_router = APIRouter()


@video_router.websocket("/connect")
async def video_connect(
        websocket: WebSocket,
        owner: Annotated[Owner | None, Depends(get_owner_data_ws)],
        device_serial_number: str | None = None,
        stream_url: str | None = None
):
    if device_serial_number is None or stream_url is None:
        service_logger.warning("WS connect missing query params")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing query params")
        return

    if not owner:
        service_logger.debug(
            f"No owner found from the jwt token. Device with number {device_serial_number}, to URL "
            f"{stream_url} attempted to connect"
        )
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION, reason="Authentication credentials is invalid"
        )
        return

    if not await check_device_ownership_ws(
            requesting_owner=owner, device_serial_number=device_serial_number
    ):
        service_logger.debug(
            f"Device with number {device_serial_number} was not found or not owned by {owner.sub}"
        )
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION, reason="Device not found"
        )
        return

    await websocket.accept()
    try:
        while True:
            await websocket.send_bytes(secrets.token_bytes(32))
            await asyncio.sleep(1 / 30)  # simulate ~30fps mock stream
    except WebSocketDisconnect:
        service_logger.debug(f"Video stream client disconnected for device {device_serial_number}")
