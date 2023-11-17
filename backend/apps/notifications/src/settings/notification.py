from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


class NotificationSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="notification_")

    email_welcome_topic_name: str = "email-welcome-event"
    email_weekly_update_topic_name: str = "email-weekly-update-event"
    email_welcome_queue_name: str = "email-welcome-queue"
    email_weekly_update_queue_name: str = "email-weekly-update-queue"
    email_group_id: str = "email"

    ws_like_topic_name: str = "ws-like-event"
    ws_like_queue_name: str = "ws-like-queue"
    ws_group_id: str = "ws"
