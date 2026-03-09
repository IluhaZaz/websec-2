from typing import Optional

from backend.src.schedule.gateway import ScheduleGateway
from backend.src.schedule.repository import ScheduleRepository
from backend.src.schemas.week import Week


class ScheduleService:
    def __init__(
            self,
            gateway: ScheduleGateway,
            repository: ScheduleRepository
    ):
        self.gateway = gateway
        self.repository = repository

    async def save_groups_ids(self):
        data = await self.gateway.get_groups_ids()

        await self.repository.set_keys(data)

        return data

    async def get_groups(self) -> list[str]:
        data = await self.repository.get_keys()
        return data

    async def get_week(self, group: str, week_num: Optional[int] = None) -> Week:
        id_ = await self.repository.get(group)
        id_ = int(id_)
        if id_ is not None:
            return await self.gateway.get_week(id_, week_num)

