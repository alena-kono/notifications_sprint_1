from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class RabbitMqSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="rabbitmq_")

    host: str
    port: int
    vhost: str
    username: str
    password: str
