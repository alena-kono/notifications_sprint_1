from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from fastapi import WebSocket

from src.schemas.in_events import InEventSchema

EventType = TypeVar("EventType", bound=InEventSchema)


class IWebsocketService(ABC):
    @abstractmethod
    async def connect(self, websocket: WebSocket, token: str) -> None:
        ...


class IRabbitMQService(ABC, Generic[EventType]):
    @abstractmethod
    async def handle_event(self, event: EventType) -> None:
        ...
