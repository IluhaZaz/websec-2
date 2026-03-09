import json
from typing import Optional

import httpx

from frontend.connections.backend.config import BackendConfig


class BackendConnection:
    def __init__(self, config: BackendConfig):
        self.api_base = f"http://{config.host}:{config.port}"

    async def get_week(
        self,
        group: str,
        week_num: Optional[int] = None
    ) -> dict:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{self.api_base}/schedule/week",
                params={
                    "group": group,
                    "week_num": week_num
                }
            )
        return json.loads(res.content)

    async def get_groups(self) -> dict[str, str]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.api_base}/schedule/groups")
        return json.loads(res.content)["groups"]