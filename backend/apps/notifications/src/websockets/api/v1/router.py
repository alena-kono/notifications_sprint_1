import structlog
from faststream import Depends
from faststream.kafka import KafkaRouter
from faststream.kafka.annotations import KafkaMessage

from src.settings.app import get_app_settings
from src.websockets import dependencies as ws_deps
from src.websockets.services import (
    WebsocketNotificationService,
    ws_service_factory,
    WebsocketServiceSchemaType,
)

settings = get_app_settings()

logger = structlog.get_logger()

router = KafkaRouter()


@router.subscriber(
    settings.notification.ws_like_topic_name,
    group_id=settings.notification.ws_group_id,
    batch=False,
    auto_commit=False,
    retry=5,
)
async def websocket_like_event_handler(
    message_payload: ws_deps.LikeEventMessage,
    msg_context: KafkaMessage,
    service: WebsocketNotificationService = Depends(
        ws_service_factory(WebsocketServiceSchemaType.like)
    ),
) -> None:
    await logger.info(
        "Message has been consumed from Kafka",
        topic_name=settings.notification.ws_like_topic_name,
        group_id=settings.notification.ws_group_id,
        message_id=msg_context.message_id,
        message_payload=message_payload,
    )

    await service.handle_events(
        event_messages=[message_payload],
        queue_name=settings.notification.ws_like_queue_name,
        msg_context=msg_context,
    )
