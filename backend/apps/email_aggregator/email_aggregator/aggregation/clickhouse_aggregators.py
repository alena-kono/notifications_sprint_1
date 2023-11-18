from asynch.connection import Connection
from asynch.cursors import DictCursor

from aiokafka.producer import AIOKafkaProducer

from email_aggregator.settings.app import AppSettings

import json


VIEWS_SQL = """
    SELECT user_id, count(distinct film_id) as watched_films_count
    FROM {table}
    WHERE toDate(timestamp) >= toDate(now()) - INTERVAL 7 DAY
    group by user_id;
"""


async def build_last_week_views(
    connection: Connection,
    producer: AIOKafkaProducer,
    settings: AppSettings
):
    async with connection.cursor(cursor=DictCursor) as cursor:
        await cursor.execute(VIEWS_SQL.format(table=settings.clickhouse.views_table))
        data = await cursor.fetchall()
        for entry in data:
            entry['user_id'] = str(entry['user_id'])
            kafka_message = json.dumps(entry).encode()
            await producer.send(
                topic=settings.kafka.views_report_topic,
                key=entry['user_id'],
                value=kafka_message
            )
