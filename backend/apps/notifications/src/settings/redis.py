import pydantic

from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class RedisSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="redis_")

    host: str
    port: int

    list_name: str = "events"

    @property
    def dsn(self) -> str:
        return str(
            pydantic.RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
            )
        )
