from typing import Optional

from src.schedule.gateway import ScheduleGateway
from src.schedule.repository import ScheduleRepository
from src.schemas.week import Week


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

    async def get_week(self, group: str, week_num: Optional[str] = None) -> Week:
        id_ = await self.repository.get(group)
        print(id_)