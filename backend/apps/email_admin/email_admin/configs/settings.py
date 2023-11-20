from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )

    template_folder: Path = BASE_DIR / "templates"

    kafka_host: str
    kafka_port: int

    service_host: str
    service_port: int
    service_description: str = "Email Admin Service"
    service_name: str = "email-admin"

    kafka_topic: str = "email-manager-event"

    auth_jwt_secret_key: str
    auth_jwt_encoding_algorithm: str = "HS256"

    db_name: str = "email_manager"
    mongo_host: str
    mongo_port: int


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
