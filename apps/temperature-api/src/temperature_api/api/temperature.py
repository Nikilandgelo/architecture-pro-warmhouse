from fastapi import APIRouter

from temperature_api.domain import TemperatureService
from temperature_api.responses import TemperatureResponse

temperature_router = APIRouter()


@temperature_router.get("/")
async def get_random_temperature(location: str) -> TemperatureResponse:
    return TemperatureService(location=location).get_data()


@temperature_router.get("/{sensor_id}")
async def get_random_temperature(sensor_id: str) -> TemperatureResponse:
    return TemperatureService(sensor_id=sensor_id).get_data()
