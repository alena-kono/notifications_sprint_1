from faststream import Depends
from faststream.rabbit import RabbitRouter

from email_worker.configs.settings import get_settings
from email_worker.schemas.events import (
    EventSchema,
    WeeklyUpdateContentSchema,
    WelcomeContentSchema,
)
from email_worker.services.service import Service, ServiceType, service_factory

router = RabbitRouter()
settings = get_settings()


@router.subscriber("welcome-event")
async def welcome_handler(
    welcome_event: list[EventSchema[WelcomeContentSchema]],
    service: Service = Depends(service_factory(ServiceType.WELCOME)),
) -> None:
    await service.handle_event(welcome_event)


@router.subscriber("weekly-update-event")
async def weekly_update_handler(
    welcome_event: list[EventSchema[WeeklyUpdateContentSchema]],
    service: Service = Depends(service_factory(ServiceType.WEEKLY_UPDATE)),
) -> None:
    await service.handle_event(welcome_event)
