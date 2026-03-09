import json
from typing import Optional

import httpx

from frontend.connections.backend.config import BackendConfig


class BackendConnection:
    def __init__(self, config: BackendConfig):
        self.api_base = f"http://{config.host}:{config.port}"
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def get_week_by_group(
        self,
        group: str,
        week_num: Optional[int] = None
    ) -> dict:
        url = f"{self.api_base}/schedule/week/group"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(
                url,
                params={
                    "group": group,
                    "week_num": week_num
                }
            )
        return json.loads(res.content)

    async def get_week_by_teacher(
        self,
        group: str,
        week_num: Optional[int] = None
    ) -> dict:
        url = f"{self.api_base}/schedule/week/teacher"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(
                url,
                params={
                    "teacher_id": group,
                    "week_num": week_num
                }
            )
        return json.loads(res.content)

    async def get_groups(self) -> dict[str, str]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            res = await client.get(f"{self.api_base}/schedule/groups")
        return json.loads(res.content)["groups"]