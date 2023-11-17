from functools import lru_cache

import pydantic

from src.settings.base import BaseAppSettings
from src.settings.kafka import KafkaSettings
from src.settings.logging import LoggingSettings
from src.settings.notification import NotificationSettings
from src.settings.rabbitmq import RabbitMqSettings
from src.settings.service import ServiceSettings


class AppSettings(BaseAppSettings):
    is_development: bool = pydantic.Field(env="IS_DEVELOPMENT", default=False)

    service: ServiceSettings = ServiceSettings()
    logging: LoggingSettings = LoggingSettings()
    notification: NotificationSettings = NotificationSettings()
    kafka: KafkaSettings = KafkaSettings()
    rabbitmq: RabbitMqSettings = RabbitMqSettings()


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()
