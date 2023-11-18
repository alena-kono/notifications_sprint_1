from contextlib import asynccontextmanager

from asynch.connection import Connection, connect

from email_aggregator.settings.clickhouse import ClickhouseSettings


@asynccontextmanager
async def clickhouse_connection(clickhouse_settings: ClickhouseSettings) -> Connection:
    connection = None
    try:
        connection = await connect(
            host=clickhouse_settings.host,
            port=clickhouse_settings.port,
            database=clickhouse_settings.database,
            user=clickhouse_settings.user,
            password=clickhouse_settings.password,
        )
        yield connection
    finally:
        if connection:
            await connection.close()
