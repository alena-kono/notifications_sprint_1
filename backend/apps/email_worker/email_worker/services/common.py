from typing import Generic, TypeVar
from uuid import UUID

from email_worker.email_builders.interface import IEmailBuilder
from email_worker.email_senders.interface import IEmailSender
from email_worker.schemas.events import EventSchema
from email_worker.schemas.user import UserSchema
from email_worker.services.interface import IService

T = TypeVar("T", bound=EventSchema)


class Service(IService, Generic[T]):
    def __init__(
        self,
        email_builder: IEmailBuilder[T],
        email_sender: IEmailSender,
    ) -> None:
        self.email_builder = email_builder
        self.email_sender = email_sender

    async def get_user(self, user_id: UUID) -> UserSchema:
        return UserSchema(id=user_id, name="User!", email="user@gmail.com")

    async def handle_event(self, event_msg: T) -> None:
        user = await self.get_user(event_msg.user_id)
        email_message = self.email_builder.build(event_msg, user)
        await self.email_sender.send(email_message)
