from aiokafka.producer import AIOKafkaProducer

from email_admin.configs.settings import get_settings

settings = get_settings()

producer: AIOKafkaProducer | None = None


def get_kafka_producer() -> AIOKafkaProducer:
    if producer is None:
        raise RuntimeError("Kafka producer has not been defined.")

    return producer
