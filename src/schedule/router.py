from typing import Optional

from fastapi import APIRouter

from src.schedule.depends import ScheduleServiceDepends
from src.schemas.week import Week

router = APIRouter(prefix="/schedule")

@router.get("/week")
async def get_week(
        group: str,
        service: ScheduleServiceDepends,
        week_num: Optional[str]=None) -> Week:
    return await service.get_week(group, week_num)

@router.post("/save_ids")
async def save_groups_ids(
        service: ScheduleServiceDepends
) -> dict[str, int]:
    return await service.save_groups_ids()