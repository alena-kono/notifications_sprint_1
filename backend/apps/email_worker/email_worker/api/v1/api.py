from faststream import Depends
from faststream.rabbit import RabbitRouter

from email_worker.configs.settings import get_settings
from email_worker.schemas.events import WelcomeEventSchema
from email_worker.services.welcome_service import WelcomeService, get_welcome_service

router = RabbitRouter()
settings = get_settings()


@router.subscriber("welcome-event")
async def welcome_handler(
    welcome_event: WelcomeEventSchema,
    service: WelcomeService = Depends(get_welcome_service),
) -> None:
    await service.handle_event(welcome_event)
