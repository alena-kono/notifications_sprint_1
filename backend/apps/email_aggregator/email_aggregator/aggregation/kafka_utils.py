from email_aggregator.settings.kafka import KafkaSettings

from aiokafka.producer import AIOKafkaProducer


async def kafka_producer(kafka_settings: KafkaSettings) -> AIOKafkaProducer:
    async with AIOKafkaProducer(
        bootstrap_servers=[kafka_settings.dsn],
        compression_type="gzip",
        enable_idempotence=True,
        max_batch_size=32768,
        linger_ms=200,
    ) as producer:
        yield producer
