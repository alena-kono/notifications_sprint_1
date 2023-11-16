from logging import config as logging_config

import structlog

from faststream import Depends
from faststream.kafka import KafkaRouter
from faststream.kafka.annotations import KafkaMessage

from src.emails import dependencies as emails_deps
from src.emails.services import (
    EmailNotificationService,
    EmailServiceSchemaType,
    email_service_factory,
)
from src.settings.app import get_app_settings
from src.settings.logging import configure_logger


settings = get_app_settings()

logging_config.dictConfig(settings.logging.config)
configure_logger(enable_async_logger=True)

logger = structlog.get_logger()

router = KafkaRouter()


@router.subscriber(
    settings.notification.email_welcome_topic_name,
    group_id=settings.notification.email_group_id,
    batch=True,
    auto_commit=False,
    retry=5,
)
async def email_welcome_event_handler(
    message_payload: list[emails_deps.WelcomeEventMessage],
    msg_context: KafkaMessage,
    service: EmailNotificationService = Depends(
        email_service_factory(EmailServiceSchemaType.welcome)
    ),
) -> None:
    await logger.info(
        "Message has been consumed from Kafka",
        topic_name=settings.notification.email_welcome_topic_name,
        group_id=settings.notification.email_group_id,
        message_id=msg_context.message_id,
        message_payload=message_payload,
    )

    await service.handle_events(
        event_messages=message_payload,
        queue_name=settings.notification.email_welcome_queue_name,
        msg_context=msg_context,
    )


@router.subscriber(
    settings.notification.email_weekly_update_topic_name,
    group_id=settings.notification.email_group_id,
    batch=True,
    auto_commit=False,
    retry=5,
)
async def email_weekly_update_event_handler(
    message_payload: list[emails_deps.WeeklyUpdateMessage],
    msg_context: KafkaMessage,
    service: EmailNotificationService = Depends(
        email_service_factory(EmailServiceSchemaType.weekly_update)
    ),
) -> None:
    await logger.info(
        "Message has been consumed from Kafka",
        topic_name=settings.notification.email_weekly_update_topic_name,
        group_id=settings.notification.email_group_id,
        message_id=msg_context.message_id,
        message_payload=message_payload,
    )

    await service.handle_events(
        event_messages=message_payload,
        queue_name=settings.notification.email_weekly_update_queue_name,
        msg_context=msg_context,
    )
