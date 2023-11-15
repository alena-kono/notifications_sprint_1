from faststream.kafka import KafkaBroker
from faststream.rabbit import RabbitBroker
import structlog
from src.settings.app import get_app_settings

settings = get_app_settings()
logger = structlog.get_logger()

broker_kafka: KafkaBroker | None = None
broker_rabbit: RabbitBroker | None = None


def get_kafka_broker() -> KafkaBroker:
    if broker_kafka is None:
        return KafkaBroker(bootstrap_servers=settings.kafka.dsn)

    return broker_kafka


def get_rabbit_broker() -> RabbitBroker:
    if broker_rabbit is None:
        raise RuntimeError("RabbitMQ broker has not been defined.")

    return broker_rabbit
