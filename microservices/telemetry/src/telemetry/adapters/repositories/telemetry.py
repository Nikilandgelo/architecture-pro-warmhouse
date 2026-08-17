from dataclasses import asdict, fields

from clickhouse_connect.driver.query import QueryResult

from telemetry.adapters.clickhouse import clickhouse_adapter, TELEMETRY_FOR_DEVICE
from telemetry.entities import TelemetryDBRecord, TelemetrySearchFields


class TelemetryRepository:

    @staticmethod
    async def insert_telemetry(data: TelemetryDBRecord) -> None:
        row = list(asdict(data).values())
        await clickhouse_adapter.client.insert(
            table=TelemetryDBRecord.__tablename__,
            data=[row],
            column_names=[f.name for f in fields(data)]
        )

    @staticmethod
    async def fetch_telemetry_records(
            searching_fields: TelemetrySearchFields,
            limit: int = 50,
            offset: int = 0
    ) -> QueryResult:
        query = TELEMETRY_FOR_DEVICE + f"\nLIMIT {limit}\n OFFSET {offset}"
        result = await clickhouse_adapter.client.query(
            query=query,
            parameters=searching_fields.model_dump()
        )
        return result
