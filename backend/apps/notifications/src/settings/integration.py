from pydantic import HttpUrl
from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class IntegrationSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="integration_")

    auth_access_jwt: str
    auth_users_url: HttpUrl
