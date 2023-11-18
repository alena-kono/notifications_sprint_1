import pydantic
from email_aggregator.settings.base import BaseAppSettings


class ClickhouseSettings(BaseAppSettings):
    host: str = pydantic.Field(env="CLICKHOUSE_HOST", default="localhost")
    port: int = pydantic.Field(env="CLICKHOUSE_PORT", default=9000)
    database: str = pydantic.Field(env="CLICKHOUSE_DB", defualt="default")
    user: str = pydantic.Field(env="CLICKHOUSE_USER", default="default")
    password: str = pydantic.Field(env="CLICKHOUSE_PASSWORD", default="")

    views_table: str = "ugc_film_views"
