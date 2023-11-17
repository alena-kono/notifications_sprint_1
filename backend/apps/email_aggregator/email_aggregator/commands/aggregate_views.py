import typer

from email_aggregator.aggregation.clickhouse_aggregators import build_last_week_views
from email_aggregator.aggregation.clickhouse_utils import clickhouse_connection
from email_aggregator.aggregation.kafka_utils import kafka_producer
from email_aggregator.settings.app import get_app_settings

import asyncio

app = typer.Typer()


async def send_views_statistics() -> None:
    settings = get_app_settings()
    async with clickhouse_connection(settings.clickhouse) as connection, kafka_producer(settings.kafka) as producer:
        await build_last_week_views(connection, producer, settings)


@app.command()
def send_statistics() -> None:
    asyncio.run(send_views_statistics())


if __name__ == '__main__':
    app()
