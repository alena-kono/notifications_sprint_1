from functools import lru_cache

from email_aggregator.settings.base import BaseAppSettings
from email_aggregator.settings.service import ServiceSettings
from email_aggregator.settings.clickhouse import ClickhouseSettings
from email_aggregator.settings.kafka import KafkaSettings


class AppSettings(BaseAppSettings):
    service = ServiceSettings()
    clickhouse = ClickhouseSettings()
    kafka = KafkaSettings()


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings()
