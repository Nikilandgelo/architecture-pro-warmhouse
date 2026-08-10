from automation_engine.broker.routers import commands_router
from automation_engine.entities import ActivityStatusPayload, DynamicValuePayload

ALL_PUBLISHERS = {
    ".devices.activity_status": commands_router.publisher(
        subject=".devices.activity_status",
        title="Activity Status Publisher",
        description="Publish command about the new status",
        schema=ActivityStatusPayload
    ),
    ".devices.dynamic_target_value": commands_router.publisher(
        subject=".devices.dynamic_target_value",
        title="Dynamic Value Publisher",
        description="Publish command about the new value",
        schema=DynamicValuePayload
    )
}
