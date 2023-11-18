import pydantic
from email_aggregator.settings.base import BaseAppSettings


class KafkaSettings(BaseAppSettings):
    host: str = pydantic.Field(env="KAFKA_HOST", default="localhost")

    port: int = pydantic.Field(env="KAFKA_PORT", default=9092)

    views_report_topic: str = "email-weekly-update-event"

    @property
    def dsn(self) -> str:
        return f"{self.host}:{self.port}"
