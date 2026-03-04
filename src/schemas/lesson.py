from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LessonType(Enum):
    practice = "practice"
    laboratory = "laboratory"
    lection = "lection"


class Lesson(BaseModel):
    name: str
    location: str
    teacher: str
    type: LessonType
    lesson_num: int
    groups: Optional[list[str]]