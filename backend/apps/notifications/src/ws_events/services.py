import asyncio
import enum

from typing import Callable, Type

import structlog

from src.common.dependencies import MessageBrokerServiceType, RepositoryType
from src.common.repositories import IRepository
from src.common.services import (
    IMessageBrokerService,
)
from src.settings.app import get_app_settings
from src.ws_events.schemas import InputLikeEvent, LikeWebsocketPush


logger = structlog.get_logger()
settings = get_app_settings()


class WebsocketServiceType(enum.StrEnum):
    like = enum.auto()


class WebsocketService:
    queue_name: str = settings.notification.ws_like_queue_name
    collection_name: str = "websockets"

    def __init__(
        self,
        repository: IRepository,
        message_broker_service: IMessageBrokerService,
    ) -> None:
        self.message_broker_service = message_broker_service
        self.repository = repository

    async def send(self, event: LikeWebsocketPush) -> None:
        await asyncio.gather(
            self.repository.insert(
                data=event.model_dump(),
                collection=self.collection_name,
            ),
            self.message_broker_service.publish(
                message_payload=event, queue_name=self.queue_name
            ),
        )

    async def build_message(self, event: InputLikeEvent) -> LikeWebsocketPush:
        return LikeWebsocketPush(user_id=event.user_id)

    async def handle_events(self, event: InputLikeEvent) -> None:
        output_event = await self.build_message(event=event)
        await self.send(event=output_event)

        await logger.info("Message has been acknowledged")


def ws_service_factory(
    service_schema_type: WebsocketServiceType
) -> Callable[[], WebsocketService]:
    schemas_mapping: dict[WebsocketServiceType, Type[WebsocketService]] = {
        WebsocketServiceType.like: WebsocketService,
    }

    def _service(
        repository: RepositoryType,
        message_broker_service: MessageBrokerServiceType,
    ) -> WebsocketService:
        if service_schema_type in schemas_mapping:
            return schemas_mapping[service_schema_type](
                repository=repository,
                message_broker_service=message_broker_service,
            )

        raise NotImplementedError

    return _service
