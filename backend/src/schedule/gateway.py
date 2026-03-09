import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from backend.src.schedule.config import GatewayConfig
from backend.src.schemas.lesson import Lesson, LessonType
from backend.src.schemas.week import Week


class ScheduleGateway:
    def __init__(self, config: GatewayConfig):
        self.api_base = config.api_base

    async def get_faculties_ids(self) -> list[str]:
        res = []
        async with httpx.AsyncClient() as session:
            faculties_page = await session.get(f"{self.api_base}/rasp")

            soup = BeautifulSoup(faculties_page.content.decode("utf-8"), 'html.parser')

            faculty_block = soup.find('div', class_='faculties')

            for item in faculty_block.find_all('div', class_='faculties__item'):
                link_tag = item.find('a')
                link = link_tag.get("href")

                match = re.search(r'/faculty/(\d+)', link)
                faculty_id = match.group(1)

                res.append(faculty_id)
        return res

    async def get_groups_ids(self) -> dict[str, int]:
        faculties_ids = await self.get_faculties_ids()

        res = dict()

        async with httpx.AsyncClient() as session:
            for faculty_id in faculties_ids:
                for course_num in range(1, 7):
                    course_link = f"{self.api_base}/rasp/faculty/{faculty_id}?course={course_num}"

                    resp = await session.get(course_link)
                    if resp.status_code == 200:
                        course_page = resp.content.decode("utf-8")

                        soup = BeautifulSoup(course_page, 'html.parser')

                        group_elems = soup.find_all(
                            "a",
                            class_="btn-text group-catalog__group"
                        )
                        course_dict = dict()
                        for group in group_elems:
                            name = group.find("span").text
                            id_ = re.search(r'groupId=(\d+)', group.get("href")).group(1)

                            course_dict[name] = int(id_)
                        res.update(course_dict)
                    else:
                        print(resp.content)
        return res

    async def get_week(self, group_id: int, week_num: Optional[int] = None) -> Week:
        schedule_link = f"{self.api_base}/rasp?groupId={group_id}"
        week = Week()

        if week_num:
            week.num = week_num
            schedule_link += f"&selectedWeek={week_num}"

        async with httpx.AsyncClient() as session:
            resp = await session.get(schedule_link)
        schedule_page = resp.content.decode("utf-8")

        soup = BeautifulSoup(schedule_page, 'html.parser')

        week_num = soup.find("span", class_="week-nav-current_week").text.strip()
        week.num = int(week_num.split()[0].strip())

        item_cnt = 0
        for item in soup.find_all("div", class_="schedule__item"):
            if "schedule__head" in item.get("class"):
                continue

            lessons_schemas = []
            lessons = item.find_all("div", class_="schedule__lesson")
            for lesson in lessons:
                type_ = lesson.find("div", class_="schedule__lesson-type-chip").text.strip()
                name = lesson.find("div", class_="schedule__discipline").text.strip()
                teacher = lesson.find("div", class_="schedule__teacher").text.strip()
                place = lesson.find("div", class_="schedule__place").text.strip()
                groups = [g.text.strip() for g in lesson.find_all("a", class_="schedule__group")]

                caption = lesson.find("span", class_="caption-text")
                if caption:
                    caption = caption.text.strip()

                lesson_schema = Lesson(
                    type=LessonType(type_),
                    lesson_indx=item_cnt % 6,
                    name=name,
                    teacher=teacher,
                    place=place,
                    groups=groups,
                    caption=caption
                )
                lessons_schemas.append(lesson_schema)

            week[item_cnt%6][item_cnt//6] = lessons_schemas

            item_cnt += 1

        return week




