from faststream import Depends
from faststream.rabbit import RabbitRouter

from email_worker.configs.settings import get_settings
from email_worker.schemas.events import EmailEvent
from email_worker.services.service import Service, service

router = RabbitRouter()
settings = get_settings()


@router.subscriber("email-queue")
async def welcome_handler(
    email_event: EmailEvent,
    service: Service = Depends(service),
) -> None:
    await service.handle_event(email_event)
