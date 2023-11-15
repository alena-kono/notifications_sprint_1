from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class ServiceSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="service_")

    name: str
    debug: bool = False

    description: str = "Notifications service"
    version: str = "0.1.0"
