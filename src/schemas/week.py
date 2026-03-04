from typing import Optional

from pydantic import BaseModel

from src.schemas.day import Day


class Week(BaseModel):
    days: list[Day]
    num: Optional[int]
