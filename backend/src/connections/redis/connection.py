from typing import Any, Optional

from redis.asyncio import Redis

from backend.src.connections.redis.config import RedisConfig


class RedisConnection:
    def __init__(self, config: RedisConfig):
        self.config = config
        self.client: Optional[Redis] = None

    async def __aenter__(self) -> Redis:
        self.client = Redis(
            host=self.config.host,
            port=self.config.port,
            db=self.config.db
        )
        return self.client

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.client.close()