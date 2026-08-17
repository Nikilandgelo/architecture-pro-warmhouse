import json

from automation_engine.adapters.repositories import ScenariosRepository
from automation_engine.broker.publishers import ALL_PUBLISHERS
from automation_engine.entities import TelemetryPayload
from automation_engine.loggers import service_logger


class TelemetryHandler:

    @classmethod
    def _check_states(cls, states: dict | None, values: dict[str, str]) -> bool:
        if states is None:
            return False

        for looking_state, value in states.items():
            if looking_state not in values:
                continue

            telemetry_value = states.get(looking_state)
            if telemetry_value == value:
                return True

        return False

    @classmethod
    def _check_metrics(cls, metrics: dict | None, values: dict[str, float]) -> bool:
        if metrics is None:
            return False

        for looking_state, value in metrics.items():
            if looking_state not in values:
                continue

            telemetry_value = metrics.get(looking_state)
            if telemetry_value == value:
                return True

        return False

    @classmethod
    async def process_telemetry_event(cls, payload: TelemetryPayload) -> None:
        matched_scenarios = await ScenariosRepository.find_scenarios_by_device(
            trigger_serial_number=payload.device_serial_number
        )
        for scenario in matched_scenarios:
            if not any([
                cls._check_states(scenario.conditions.get("states"), payload.states),
                cls._check_metrics(scenario.conditions.get("metrics"), payload.metrics)
            ]):
                service_logger.debug(
                    f"All checks have been failed, {scenario.conditions=} for payload "
                    f"{payload.model_dump()}"
                )
                continue

            for action in scenario.actions:
                action_command_extra_data = action.get("action_command_extra_data") or {}
                if len(action_command_extra_data) == 0:
                    service_logger.debug(f"Action command extra data is empty, {action=}")
                    continue

                subject = action_command_extra_data.get("subject", "")
                publisher = ALL_PUBLISHERS.get(subject)
                if not publisher:
                    service_logger.debug(f"Publisher was not found for {action=}")
                    continue

                message_data = action_command_extra_data.get("additional_data") or {}
                if len(message_data) == 0:
                    service_logger.debug(f"Additional data is empty, {action=}")
                    continue

                await publisher.publish(
                    message=json.dumps(
                        obj=message_data | {"device_serial_number": action["target_serial_number"]}
                    ).encode()
                )
