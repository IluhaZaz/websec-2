from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendConfig(BaseSettings):
    host: str = "localhost"
    port: int = 7000

    model_config = SettingsConfigDict(
        env_prefix="backend_"
    )