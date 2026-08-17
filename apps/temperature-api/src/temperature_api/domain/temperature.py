from secrets import randbelow

from temperature_api.responses import TemperatureResponse


class TemperatureService:

    def __init__(self, sensor_id: str | None = None, location: str | None = None) -> None:
        self.sensor_id = sensor_id
        self.location = location

    def _get_sensor_id(self) -> str:
        if self.sensor_id:
            return self.sensor_id

        match self.location:
            case "Living Room":
                return "1"
            case "Bedroom":
                return "2"
            case "Kitchen":
                return "3"
            case _:
                return "0"

    def _get_location(self) -> str:
        if self.location:
            return self.location

        match self.sensor_id:
            case "1":
                return "Living Room"
            case "2":
                return "Bedroom"
            case "3":
                return "Kitchen"
            case _:
                return "Unknown"

    def get_data(self) -> TemperatureResponse:
        return TemperatureResponse(
            value=randbelow(50),
            sensor_id=self._get_sensor_id(),
            location=self._get_location(),
        )
