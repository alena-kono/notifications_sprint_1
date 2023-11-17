from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from src.configs.settings import get_settings
from src.schemas.in_events import InLikeEventSchema
from src.services.interfaces import IRabbitMQService
from src.services.rabbit_service import get_rabbitmq_service

settings = get_settings()

rabbit_router = RabbitRouter(
    host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    login=settings.rabbitmq_username,
    password=settings.rabbitmq_password,
    virtualhost=settings.rabbitmq_vhost,
    schema_url="/asyncapi",
    include_in_schema=True,
)


@rabbit_router.subscriber("ws-like-queue")
async def like_event_handler(
    like_event: InLikeEventSchema,
    service: IRabbitMQService = Depends(get_rabbitmq_service),
):
    await service.handle_event(like_event)
