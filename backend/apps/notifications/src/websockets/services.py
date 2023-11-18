import enum
from typing import Callable, Type

import structlog
from faststream import Depends
from faststream.kafka.annotations import KafkaMessage

from src.common import dependencies as common_deps
from src.common.services import (
    IMessageBrokerService,
    NotificationService,
    get_message_broker_service,
)
from src.users.services import IUserService, get_user_service
from src.websockets import schemas as ws_schemas

logger = structlog.get_logger()


class WebsocketServiceSchemaType(enum.StrEnum):
    like = enum.auto()


class WebsocketNotificationService(NotificationService):
    def __init__(
        self,
        user_service: IUserService,
        message_broker_service: IMessageBrokerService,
        schema_cls: Type[ws_schemas.WebsocketPush],
    ) -> None:
        super().__init__(user_service)
        self.message_broker_service = message_broker_service
        self.schema_cls = schema_cls

    async def handle_events(
        self,
        event_messages: list[common_deps.EventMessage],
        queue_name: str,
        msg_context: KafkaMessage,
    ) -> None:
        event_users_ids = [msg.user_id for msg in event_messages]

        users_existing = await self.user_service.get_users(users_ids=event_users_ids)
        users_existing_map = {str(user.id): user for user in users_existing}

        ws_push_notifications = []
        event_messages_non_existing_users = []

        if users_existing:
            for msg in event_messages:
                # TODO: Check user notification preferences
                if users_existing_map.get(msg.user_id):
                    ws_push_notifications.append(self.schema_cls(user_id=msg.user_id))
                else:
                    event_messages_non_existing_users.append(msg)

            for push_msg in ws_push_notifications:
                await self.message_broker_service.publish(
                    message_payload=push_msg, queue_name=queue_name
                )

            if event_messages_non_existing_users:
                await logger.info(
                    "There are event messages related to non-existing users",
                    event_messages=event_messages_non_existing_users,
                )
        else:
            await logger.info("Users do not exist", users_ids=event_users_ids)

        await msg_context.ack()
        await logger.info(
            "Message has been acknowledged", message_id=msg_context.message_id
        )


def ws_service_factory(
    service_schema_type: WebsocketServiceSchemaType
) -> Callable[[], WebsocketNotificationService]:
    schemas_mapping = {
        service_schema_type.like.value: ws_schemas.LikeWebsocketPush,
    }

    def _service(
        user_service=Depends(get_user_service),
        message_broker_service=Depends(get_message_broker_service),
    ) -> WebsocketNotificationService:
        if matching_schema := schemas_mapping.get(service_schema_type.value):
            return WebsocketNotificationService(
                user_service=user_service,
                message_broker_service=message_broker_service,
                schema_cls=matching_schema,
            )
        raise NotImplementedError

    return _service
