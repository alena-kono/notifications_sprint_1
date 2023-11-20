import structlog

from faststream.kafka import KafkaBroker
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue

from src.settings.app import get_app_settings


settings = get_app_settings()
logger = structlog.get_logger()

broker_kafka: KafkaBroker | None = None
broker_rabbit: RabbitBroker | None = None


def get_rabbit_broker() -> RabbitBroker:
    if broker_rabbit is None:
        raise RuntimeError("RabbitMQ broker has not been defined.")

    return broker_rabbit


async def create_rabbit_queues() -> None:
    if broker_rabbit is None:
        raise RuntimeError("RabbitMQ broker has not been defined.")

    queues_to_declare = (
        settings.notification.email_queue,
        settings.notification.ws_like_queue_name,
    )
    for queue_name in queues_to_declare:
        await broker_rabbit.declare_queue(queue=RabbitQueue(queue_name))


async def declare_rabbit_exchange() -> None:
    if broker_rabbit is None:
        raise RuntimeError("RabbitMQ broker has not been defined.")

    await broker_rabbit.declare_exchange(
        exchange=RabbitExchange(
            name="notifications",
            type=ExchangeType.DIRECT,
            routing_key="",
        )
    )
