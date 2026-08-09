from telemetry.broker import events_router
from telemetry.entities import TelemetryPayload

telemetry_publisher = events_router.publisher(
    subject=".telemetry",
    title="Telemetry Publisher",
    description="Publish event about new telemetry data",
    schema=TelemetryPayload
)
