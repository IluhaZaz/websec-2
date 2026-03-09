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
    teacher: Optional[str] = None
    teacher_id: Optional[str] = None
    type: LessonType
    lesson_indx: int
    caption: Optional[str] = None
    groups: Optional[list[str]] = None