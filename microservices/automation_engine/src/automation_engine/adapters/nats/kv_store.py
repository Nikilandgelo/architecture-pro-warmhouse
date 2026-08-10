import nats
from nats.aio.client import Client
from nats.js.kv import KeyValue

from automation_engine.settings import settings


class KVStore:

    def __init__(self, key_value_name: str) -> None:
        self.nats_client: Client = None
        self.nats_key_value: KeyValue = None

        self._key_value_name = key_value_name

    async def _prepare_client(self) -> None:
        if self.nats_client is not None:
            return

        self.nats_client = await nats.connect(settings.nats_url)

    async def _prepare_bucket(self) -> None:
        if self.nats_key_value is not None:
            return

        self.nats_key_value = await self.nats_client.jetstream().key_value(self._key_value_name)

    async def startup(self) -> None:
        await self._prepare_client()
        await self._prepare_bucket()

    async def shutdown(self) -> None:
        if self.nats_client is None:
            return

        try:
            await self.nats_client.close()
        except Exception:
            pass
        finally:
            self.nats_client = None
            self.nats_key_value = None

    async def get(self, key: str) -> KeyValue.Entry:
        return await self.nats_key_value.get(key=key)

    async def put(self, key: str, value: str) -> int:
        return await self.nats_key_value.put(key=key, value=value.encode())

    async def delete(self, key: str) -> bool:
        return await self.nats_key_value.delete(key=key)


devices_kv_store = KVStore(settings.nats_key_value)
