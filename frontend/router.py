from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from frontend.depends import BackendConnectionDepends

router = APIRouter()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/")
async def index(request: Request, backend: BackendConnectionDepends):
    groups = await backend.get_groups()
    print(type(groups))
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "groups": groups
        }
    )

@router.get("/week")
async def get_week_table(
    request: Request,
    group: str,
    backend: BackendConnectionDepends,
    week_num: Optional[str]=None,
) -> templates.TemplateResponse:
    week = await backend.get_week(group, week_num)
    return templates.TemplateResponse(
        "schedule_table.html",
        {
            "request": request,
            "week": week
        }
    )