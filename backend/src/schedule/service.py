from typing import Optional

from fastapi import HTTPException

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

    async def save_groups_ids(self) -> dict[str, int]:
        data = await self.gateway.get_groups_ids()

        await self.repository.set_keys(data)

        return data

    async def get_groups(self) -> list[str]:
        data = await self.repository.get_keys()
        return data

    async def get_week_by_group(
            self,
            group: str,
            week_num: Optional[int] = None
    ) -> Week:
        id_ = await self.repository.get(group)
        id_ = id_.decode("utf-8")
        if id_ is not None:
            return await self.gateway.get_week(id_, week_num)
        raise HTTPException(404, f"No such group {group}")

    async def get_week_by_teacher_id(
            self,
            teacher_id: str,
            week_num: Optional[int] = None
    ) -> Week:
            return await self.gateway.get_week(teacher_id, week_num, is_group_id=False)

