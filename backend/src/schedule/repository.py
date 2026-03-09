from typing import Any

from backend.src.connections.redis.connection import RedisConnection


class ScheduleRepository:
    def __init__(self, redis: RedisConnection):
        self.redis = redis

    async def set(self, key: Any, value: Any) -> None:
        async with self.redis as client:
            await client.set(key, value)

    async def set_keys(self, data: dict):
        for key, val in data.items():
            await self.set(key, val)

    async def get_keys(self) -> list[str]:
        async with self.redis as client:
            keys = await client.keys("*")
        keys = [key.decode("utf-8") for key in keys]
        return keys

    async def get(self, key: Any) -> Any:
        async with self.redis as client:
            return await client.get(key)

