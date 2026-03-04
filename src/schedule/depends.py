from typing import Annotated

from fastapi import Depends

from src.connections.redis.config import RedisConfig
from src.connections.redis.connection import RedisConnection
from src.schedule.config import GatewayConfig
from src.schedule.gateway import ScheduleGateway
from src.schedule.repository import ScheduleRepository
from src.schedule.service import ScheduleService


async def get_redis() -> RedisConnection:
    yield RedisConnection(RedisConfig())

RedisDepends = Annotated[RedisConnection, Depends(get_redis)]


async def get_schedule_repository(redis: RedisDepends) -> ScheduleRepository:
        yield ScheduleRepository(redis)

ScheduleRepositoryDepends = Annotated[ScheduleRepository, Depends(get_schedule_repository)]


async def get_schedule_gateway() -> ScheduleGateway:
    yield ScheduleGateway(GatewayConfig())

ScheduleGatewayDepends = Annotated[ScheduleGateway, Depends(get_schedule_gateway)]


async def get_schedule_service(
        repository: ScheduleRepositoryDepends,
        gateway: ScheduleGatewayDepends
) -> ScheduleService:
    yield ScheduleService(gateway, repository)

ScheduleServiceDepends = Annotated[ScheduleService, Depends(get_schedule_service)]