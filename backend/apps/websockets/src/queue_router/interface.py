from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import WebSocket


class IRouter(ABC):
    @abstractmethod
    def register(self, id_: UUID, websocket: WebSocket) -> None:
        """creates a queue for the given id"""
        ...

    @abstractmethod
    async def get(self, id_: UUID) -> list[WebSocket]:
        ...
