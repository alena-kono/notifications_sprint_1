from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from email_worker.schemas.events import EventSchema

T = TypeVar("T", bound=EventSchema)


class IService(ABC, Generic[T]):
    @abstractmethod
    async def handle_event(self, event_msg: T) -> None:
        ...
