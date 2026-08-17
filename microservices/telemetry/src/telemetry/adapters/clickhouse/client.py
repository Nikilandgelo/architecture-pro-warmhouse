import clickhouse_connect
from clickhouse_connect.driver import AsyncClient

from telemetry.settings import settings


class ClickhouseAdapter:

    def __init__(self):
        self.client: AsyncClient | None = None

    async def startup(self) -> None:
        if self.client is not None:
            return

        self.client = await clickhouse_connect.get_async_client(
            host=settings.clickhouse_host,
            username=settings.clickhouse_username,
            password=settings.clickhouse_password,
            database=settings.clickhouse_database,
            port=settings.clickhouse_port,
        )

    async def shutdown(self) -> None:
        if self.client is None:
            return

        await self.client.close()

clickhouse_adapter = ClickhouseAdapter()
