from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )

    email_from: str

    template_folder: Path = BASE_DIR / "email_worker" / "templates"

    smtp_host: str
    smtp_port: int

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_vhost: str
    rabbitmq_username: str
    rabbitmq_password: str


@lru_cache(maxsize=1)
def get_settings():
    return Settings()
