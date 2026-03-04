from pydantic_settings import BaseSettings


class GatewayConfig(BaseSettings):
    api_base: str = "https://ssau.ru"
