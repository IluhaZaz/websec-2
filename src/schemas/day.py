from pydantic import BaseModel

from src.schemas.lesson import Lesson


class Day(BaseModel):
    lessons: list[list[Lesson]] = [None for _ in range(6)]

    def __getitem__(self, index):
        return self.lessons[index]

    def __len__(self):
        return len(self.lessons)

    def __setitem__(self, index, value):
        self.lessons[index] = value