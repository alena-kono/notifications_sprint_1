from abc import ABC, abstractmethod
from typing import Any
import structlog
from faststream import Depends
from faststream.kafka.annotations import KafkaMessage
from faststream.rabbit import RabbitBroker

from src.common import dependencies as common_deps
from src.users.services import IUserService
from src.common.brokers import get_rabbit_broker

logger = structlog.get_logger()


class INotificationService(ABC):
    @abstractmethod
    async def handle_events(
        self,
        event_messages: list[common_deps.EventMessage],
        queue_name: str,
        msg_context: KafkaMessage,
    ) -> None:
        ...


class NotificationService(INotificationService):
    def __init__(self, user_service: IUserService) -> None:
        self.user_service = user_service

    async def handle_events(
        self,
        event_messages: list[common_deps.EventMessage],
        queue_name: str,
        msg_context: KafkaMessage,
    ) -> None:
        ...


class IMessageBrokerService(ABC):
    @abstractmethod
    async def publish(self, message_payload: Any, queue_name: str) -> None:
        ...


class RabbitMQMessageBrokerService(IMessageBrokerService):
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker

    async def publish(self, message_payload: Any, queue_name: str) -> None:
        response_from_publisher = await self.broker.publish(
            message=message_payload, queue=queue_name
        )

        await logger.info(
            "Message has been published to RabbitMQ",
            message_payload=message_payload,
            queue_name=queue_name,
            response_from_publisher=response_from_publisher,
        )


def get_message_broker_service(
    broker: RabbitBroker = Depends(get_rabbit_broker)
) -> IMessageBrokerService:
    return RabbitMQMessageBrokerService(broker=broker)
