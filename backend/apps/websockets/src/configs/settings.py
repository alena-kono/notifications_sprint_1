from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    jwt_secret_key: str
    jwt_encoding_algorithm: str

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_username: str
    rabbitmq_password: str
    rabbitmq_vhost: str

    service_name: str
    service_version: str
    service_description: str
    service_port: int
    service_debug: bool
    service_host: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
