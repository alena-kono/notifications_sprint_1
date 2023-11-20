import structlog

from faststream.kafka.fastapi import KafkaRouter

from src.settings.app import get_app_settings
from src.ws_events.dependencies import LikeWebsocketServiceType
from src.ws_events.schemas import InputLikeEvent


settings = get_app_settings()

logger = structlog.get_logger()

router = KafkaRouter(bootstrap_servers=settings.kafka.dsn)


@router.subscriber(
    "ws-like-event",
    group_id="ws",
    batch=False,
    auto_commit=False,
    retry=5,
)
async def websocket_like_event_handler(
    message_payload: InputLikeEvent,
    service: LikeWebsocketServiceType,
) -> None:
    await service.handle_events(event=message_payload)
