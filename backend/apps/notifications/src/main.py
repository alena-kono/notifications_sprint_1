import asyncio
from logging import config as logging_config

import structlog
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.common import brokers
from src.emails.api.v1.router import router as email_router
from src.settings.app import get_app_settings
from src.settings.logging import configure_logger
from src.websockets.api.v1.router import router as ws_router

settings = get_app_settings()

logging_config.dictConfig(settings.logging.config)
configure_logger(enable_async_logger=True)

logger = structlog.get_logger()

broker = brokers.get_kafka_broker()

app = FastStream(
    broker=broker,
    title=settings.service.name,
    description=settings.service.description,
    version=settings.service.version,
)


@app.on_startup
async def on_startup() -> None:
    brokers.broker_kafka = app.broker
    brokers.broker_rabbit = RabbitBroker(
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.username,
        password=settings.rabbitmq.password,
        virtualhost=settings.rabbitmq.vhost,
    )
    await brokers.broker_kafka.connect()

    await brokers.broker_rabbit.connect()
    await brokers.create_rabbit_queues()
    await brokers.declare_rabbit_exchange()


@app.on_shutdown
async def on_shutdown() -> None:
    if brokers.broker_kafka is not None:
        await brokers.broker_kafka.close()

    if brokers.broker_rabbit is not None:
        await brokers.broker_rabbit.close()


broker.include_router(email_router)
broker.include_router(ws_router)


if __name__ == "__main__":
    asyncio.run(app.run())
