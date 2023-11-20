import structlog

from faststream.kafka.fastapi import KafkaRouter

from src.emails.dependencies import (
    ManagerEmailService,
    WeeklyUpdateEmailService,
    WelcomeEmailService,
)
from src.emails.schemas import (
    InputManagerEvent,
    InputWeeklyUpdateEvent,
    InputWelcomeEvent,
)
from src.settings.app import get_app_settings


settings = get_app_settings()

logger = structlog.get_logger()

router = KafkaRouter(bootstrap_servers=settings.kafka.dsn)


@router.subscriber(
    "email-welcome-event",
    group_id="email",
    batch=False,
    auto_commit=False,
)
async def email_welcome_event_handler(
    message_payload: InputWelcomeEvent,
    service: WelcomeEmailService,
) -> None:
    await service.handle_events(event_messages=message_payload)


@router.subscriber(
    "email-weekly-update-event",
    group_id="email",
    batch=False,
    auto_commit=False,
    retry=5,
)
async def email_weekly_update_event_handler(
    message_payload: InputWeeklyUpdateEvent,
    service: WeeklyUpdateEmailService,
) -> None:
    await service.handle_events(event_messages=message_payload)


@router.subscriber(
    "email-manager-event",
    group_id="email",
    batch=False,
    auto_commit=False,
    retry=5,
)
async def email_manager_event_handler(
    message_payload: InputManagerEvent,
    service: ManagerEmailService,
) -> None:
    await service.handle_events(event_messages=message_payload)
