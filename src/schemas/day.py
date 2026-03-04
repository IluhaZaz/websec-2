from pydantic import BaseModel

from src.schemas.lesson import Lesson


class Day(BaseModel):
    lessons: list[Lesson]
