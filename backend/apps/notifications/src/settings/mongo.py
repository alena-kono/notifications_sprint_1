from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class MongoSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="mongo_")

    host: str
    port: int
    db_name: str

    @property
    def dsn(self) -> str:
        return f"{self.host}:{self.port}"
