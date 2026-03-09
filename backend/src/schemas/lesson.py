from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LessonType(Enum):
    practice = "Практика"
    laboratory = "Лабораторная"
    lection = "Лекция"
    other = "Другое"


class Lesson(BaseModel):
    name: str
    place: str
    teacher: str
    type: LessonType
    lesson_indx: int
    caption: Optional[str] = None
    groups: Optional[list[str]] = None