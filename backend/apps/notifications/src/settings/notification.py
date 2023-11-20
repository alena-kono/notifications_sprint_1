from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class NotificationSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="notification_")

    email_queue: str = "email-queue"
    ws_like_queue_name: str = "ws-like-queue"
