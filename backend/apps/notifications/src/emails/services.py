import enum
from typing import Type, Callable

import structlog
from faststream.kafka.annotations import KafkaMessage
from faststream.rabbit import RabbitBroker

from src.common.brokers import get_rabbit_broker
from src.common.services import NotificationService, IUserService, get_user_service
from src.emails import dependencies as emails_deps
from src.emails import schemas as emails_schemas

logger = structlog.get_logger()


class EmailServiceSchemaType(enum.StrEnum):
    welcome = enum.auto()
    weekly_update = enum.auto()


class EmailNotificationService(NotificationService):
    def __init__(
        self,
        user_service: IUserService,
        broker: RabbitBroker,
        schema_cls: Type[emails_schemas.IEmail],
    ) -> None:
        super().__init__(user_service)
        self.broker = broker
        self.schema_cls = schema_cls

    async def handle_events(
        self,
        event_messages: list[emails_deps.EventMessageType],
        queue_name: str,
        msg_context: KafkaMessage,
    ) -> None:
        # TODO: Implement real handling, below is a toy implementation
        users = await self._get_users(users_ids=[msg.user_id for msg in event_messages])
        emails = []
        for msg in event_messages:
            for user in users:
                if user.id == msg.user_id:
                    emails.append(self.schema_cls.create(user=user, event_message=msg))

        response_from_publisher = await self.broker.publish(
            message=emails,
            queue=queue_name,
            # TODO: Setup exchange
            # exchange=RabbitExchange(
            #     name=queue_name,
            #     type=ExchangeType.DIRECT,
            #     routing_key="",
            # ),
        )

        await logger.info(
            "Message has been published to RabbitMQ",
            message_id=msg_context.message_id,
            message_payload=emails,
            queue_name=queue_name,
            response_from_publisher=response_from_publisher,
        )

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

    def _service() -> EmailNotificationService:
        if matching_schema := schemas_mapping.get(service_schema_type.value):
            return EmailNotificationService(
                user_service=get_user_service(),
                broker=get_rabbit_broker(),
                schema_cls=matching_schema,
            )
        raise NotImplementedError

    return _service
