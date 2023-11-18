import pydantic
from email_aggregator.settings.base import BaseAppSettings


class ServiceSettings(BaseAppSettings):
    host: str = pydantic.Field(env="SERVICE_HOST")
    port: int = pydantic.Field(env="SERVICE_PORT")
