import enum
from typing import Type, Callable

import structlog
from faststream import Depends
from faststream.kafka.annotations import KafkaMessage

from src.common import dependencies as common_deps
from src.common.services import (
    NotificationService,
    IMessageBrokerService,
    get_message_broker_service,
)
from src.emails import schemas as emails_schemas
from src.users.services import IUserService, get_user_service

logger = structlog.get_logger()


class EmailServiceSchemaType(enum.StrEnum):
    welcome = enum.auto()
    weekly_update = enum.auto()


class EmailNotificationService(NotificationService):
    def __init__(
        self,
        user_service: IUserService,
        message_broker_service: IMessageBrokerService,
        schema_cls: Type[emails_schemas.IEmail],
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

        emails = []
        event_messages_non_existing_users = []

        if users_existing:
            for msg in event_messages:
                # TODO: Check user notification preferences
                if user := users_existing_map.get(msg.user_id):
                    emails.append(self.schema_cls.create(user=user, event_message=msg))
                else:
                    event_messages_non_existing_users.append(msg)

            await self.message_broker_service.publish(
                message_payload=emails, queue_name=queue_name
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


def email_service_factory(
    service_schema_type: EmailServiceSchemaType
) -> Callable[[], EmailNotificationService]:
    schemas_mapping = {
        service_schema_type.welcome.value: emails_schemas.WelcomeEmail,
        service_schema_type.weekly_update.value: emails_schemas.WeeklyUpdateEmail,
    }

    def _service(
        user_service=Depends(get_user_service),
        message_broker_service=Depends(get_message_broker_service),
    ) -> EmailNotificationService:
        if matching_schema := schemas_mapping.get(service_schema_type.value):
            return EmailNotificationService(
                user_service=user_service,
                message_broker_service=message_broker_service,
                schema_cls=matching_schema,
            )
        raise NotImplementedError

    return _service
