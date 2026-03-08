from typing import Optional

from pydantic import BaseModel

from src.schemas.day import Day


class Week(BaseModel):
    days: list[Day] = [Day() for _ in range(6)]
    num: Optional[int] = None

    def __getitem__(self, index):
        return self.days[index]

    def __len__(self):
        return len(self.days)

    def __setitem__(self, index, value):
        self.days[index] = value