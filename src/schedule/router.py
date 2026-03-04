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