from functools import lru_cache

import pydantic

from src.settings.auth import AuthSettings
from src.settings.base import BaseAppSettings
from src.settings.integration import IntegrationSettings
from src.settings.jinja2 import Jinja2Settings
from src.settings.kafka import KafkaSettings
from src.settings.logging import LoggingSettings
from src.settings.mongo import MongoSettings
from src.settings.notification import NotificationSettings
from src.settings.rabbitmq import RabbitMqSettings
from src.settings.rate_limiter import RateLimiterSettings
from src.settings.redis import RedisSettings
from src.settings.service import ServiceSettings


class AppSettings(BaseAppSettings):
    is_development: bool = pydantic.Field(env="IS_DEVELOPMENT", default=False)

    service: ServiceSettings = ServiceSettings()  # type: ignore
    logging: LoggingSettings = LoggingSettings()  # type: ignore
    notification: NotificationSettings = NotificationSettings()  # type: ignore
    integration: IntegrationSettings = IntegrationSettings()  # type: ignore
    kafka: KafkaSettings = KafkaSettings()  # type: ignore
    rabbitmq: RabbitMqSettings = RabbitMqSettings()  # type: ignore
    rate_limiter: RateLimiterSettings = RateLimiterSettings()  # type: ignore
    mongo: MongoSettings = MongoSettings()  # type: ignore
    auth: AuthSettings = AuthSettings()  # type: ignore
    redis: RedisSettings = RedisSettings()  # type: ignore
    jinja2: Jinja2Settings = Jinja2Settings()  # type: ignore


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()
