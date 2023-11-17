from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class KafkaSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="kafka_")

    host: str
    port: int

    @property
    def dsn(self) -> str:
        return f"{self.host}:{self.port}"
