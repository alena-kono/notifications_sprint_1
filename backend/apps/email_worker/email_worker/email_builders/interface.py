from abc import ABC, abstractmethod
from email.message import EmailMessage
from typing import Generic, TypeVar

from email_worker.schemas.events import EventSchema
from email_worker.schemas.user import UserSchema

T = TypeVar("T", bound=EventSchema)


class IEmailBuilder(ABC, Generic[T]):
    @abstractmethod
    def build(self, event_msg: T, user: UserSchema) -> EmailMessage:
        ...
