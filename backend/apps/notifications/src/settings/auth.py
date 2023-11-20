from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class AuthSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="auth_")

    jwt_encoding_algorithm: str = "HS256"
    jwt_secret_key: str

    access_token_expires_secs: int
    refresh_token_expires_secs: int
