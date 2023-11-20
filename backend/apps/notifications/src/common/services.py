from abc import ABC, abstractmethod
from typing import Any, Coroutine

import structlog

from fastapi import Depends
from faststream.rabbit import RabbitBroker

from src.common import schemas as common_schemas
from src.common.brokers import get_rabbit_broker
from src.common.client import APIClient, get_api_client


logger = structlog.get_logger()


class IUserService(ABC):
    @abstractmethod
    async def get_users(
        self,
        users_ids: list[str],
    ) -> list[common_schemas.User]:
        ...


class UserService(IUserService):
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client

    async def get_users(
        self, users_ids: list[str]
    ) -> [Coroutine, None, list[common_schemas.User]]:
        ids_query = "&".join([f"ids={user_id}" for user_id in users_ids])

        response_data = await self.api_client.get(path=f"?{ids_query}")

        return [common_schemas.User(**user) for user in response_data]


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


def get_user_service(
    api_client: APIClient = Depends(get_api_client),
) -> IUserService:
    return UserService(api_client=api_client)
