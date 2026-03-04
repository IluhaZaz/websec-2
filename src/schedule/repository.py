from typing import Any

from src.connections.redis.connection import RedisConnection


class ScheduleRepository:
    def __init__(self, redis: RedisConnection):
        self.redis = redis

    async def set(self, key: Any, value: Any) -> None:
        async with self.redis as client:
            await client.set(key, value)

    async def set_keys(self, data: dict):
        for key, val in data.items():
            await self.set(key, val)

    async def get(self, key: Any) -> Any:
        async with self.redis as client:
            return await client.get(key)

