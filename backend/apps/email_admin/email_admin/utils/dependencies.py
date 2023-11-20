from typing import Annotated

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from motor.core import AgnosticClient

from email_admin.configs.kafka import get_kafka_producer
from email_admin.configs.mongo import get_mongodb
from email_admin.configs.settings import get_settings
from email_admin.utils.authorization import JWTBearer, JwtClaims
from email_admin.utils.message_queue import IMessageQueue, KafkaMessageQueue
from email_admin.utils.repositories import IRepository, MongoRepository

settings = get_settings()

KafkaProducerType = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
MongoCLientType = Annotated[AgnosticClient, Depends(get_mongodb)]


def get_message_queue(kafka_producer: KafkaProducerType) -> IMessageQueue:
    return KafkaMessageQueue(kafka_producer=kafka_producer)


def get_repository(mongo_client: MongoCLientType) -> IRepository:
    return MongoRepository(
        mongo_client=mongo_client,
        db_name=settings.db_name,
    )


UserToken = Annotated[JwtClaims, Depends(JWTBearer())]
RepositoryType = Annotated[IRepository, Depends(get_repository)]
MessageQueueType = Annotated[IMessageQueue, Depends(get_message_queue)]
