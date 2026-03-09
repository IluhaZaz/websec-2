from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from frontend.depends import BackendConnectionDepends

router = APIRouter()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/")
async def index(request: Request, backend: BackendConnectionDepends) -> _TemplateResponse:
    groups = await backend.get_groups()
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "groups": groups
        }
    )

@router.get("/week/group")
async def get_week_table_by_group(
    request: Request,
    group: str,
    backend: BackendConnectionDepends,
    week_num: Optional[str] = None
) -> _TemplateResponse:
    week = await backend.get_week_by_group(group, week_num)
    return templates.TemplateResponse(
        "schedule_table.html",
        {
            "request": request,
            "week": week
        }
    )

@router.get("/week/teacher")
async def get_week_table_by_teacher(
    request: Request,
    teacher_id: str,
    backend: BackendConnectionDepends,
    week_num: Optional[str] = None
) -> _TemplateResponse:
    week = await backend.get_week_by_teacher(teacher_id, week_num)
    return templates.TemplateResponse(
        "schedule_table.html",
        {
            "request": request,
            "week": week
        }
    )