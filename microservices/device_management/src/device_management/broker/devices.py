from faststream import AckPolicy
from faststream.nats import NatsRouter, PullSub
from nats.js.errors import KeyNotFoundError

from device_management.adapters.nats import (
    COMMANDS_STREAM,
    BASE_CONSUMER_CONFIG,
    MAX_TASKS_PER_WORKER
)
from device_management.adapters.nats import devices_kv_store
from device_management.entities.device import ActivityStatusPayload, DynamicTargetValuePayload
from device_management.handlers import DeviceHandler
from device_management.loggers import service_logger
from device_management.settings import settings

# ack_policy can't be in commands_router or events_router that are in the level above, including
# routers like this one it must be only in routers that have subscribers
devices_router = NatsRouter(prefix=".devices", ack_policy=AckPolicy.NACK_ON_ERROR)

@devices_router.subscriber(
    subject=".activity_status",
    durable=f"{COMMANDS_STREAM.name}-devices-activity-status-pull-consumer",
    stream=COMMANDS_STREAM,
    pull_sub=PullSub(batch_size=settings.max_tasks_per_worker, timeout=0.5),
    config=BASE_CONSUMER_CONFIG,
    max_workers=settings.max_tasks_per_worker,
    title="ActivityStatusCommand",
)
async def handle_activity_status_command(payload: ActivityStatusPayload) -> None:
    async with MAX_TASKS_PER_WORKER:
        try:
            await devices_kv_store.get(key=payload.device_serial_number)
        except KeyNotFoundError:
            service_logger.warning(
                f"Device with number {payload.device_serial_number} doesn't exist, but command to "
                f"change status '{payload.activity_status}' was called."
            )
            return

        await DeviceHandler.change_activity_status(
            device_serial_number=payload.device_serial_number,
            new_status=payload.activity_status
        )

@devices_router.subscriber(
    subject=".dynamic_target_value",
    durable=f"{COMMANDS_STREAM.name}-devices-dynamic-target-value-pull-consumer",
    stream=COMMANDS_STREAM,
    pull_sub=PullSub(batch_size=settings.max_tasks_per_worker, timeout=0.5),
    config=BASE_CONSUMER_CONFIG,
    max_workers=settings.max_tasks_per_worker,
    title="DynamicTargetValueCommand",
)
async def handle_target_value_command(payload: DynamicTargetValuePayload) -> None:
    async with MAX_TASKS_PER_WORKER:
        try:
            await devices_kv_store.get(key=payload.device_serial_number)
        except KeyNotFoundError:
            service_logger.warning(
                f"Device with number {payload.device_serial_number} doesn't exist, but command to change "
                f"value '{payload.new_value}' was called."
            )
            return

        await DeviceHandler.change_target_value(
            device_serial_number=payload.device_serial_number,
            new_value=payload.new_value
        )
