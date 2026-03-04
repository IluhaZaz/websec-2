import asyncio
import re

import httpx
from bs4 import BeautifulSoup

from src.schedule.config import GatewayConfig


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
        print(res)
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

                            course_dict[name] = id_
                        res.update(course_dict)
                    else:
                        print(resp.content)
        return res

