from typing import Annotated

from fastapi import Depends

from frontend.connections.backend.config import BackendConfig
from frontend.connections.backend.connection import BackendConnection


async def get_backend_config() -> BackendConfig:
    yield BackendConfig()

BackendConfigDepends = Annotated[BackendConfig, Depends(get_backend_config)]


async def get_backend(config: BackendConfigDepends) -> BackendConnection:
    yield BackendConnection(config)

BackendConnectionDepends = Annotated[BackendConnection, Depends(get_backend)]