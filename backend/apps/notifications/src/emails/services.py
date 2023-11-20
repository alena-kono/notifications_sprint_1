import asyncio
import enum

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Type, TypeVar

import structlog

from src.common.dependencies import (
    MessageBrokerServiceType,
    RepositoryType,
    UserServiceType,
)
from src.common.repositories import IRepository
from src.common.schemas import User
from src.common.services import (
    IMessageBrokerService,
    IUserService,
)
from src.emails.jinja2 import get_template
from src.emails.schemas import (
    EmailMessage,
    InputEvent,
    InputManagerEvent,
    InputWeeklyUpdateEvent,
    InputWelcomeEvent,
)
from src.settings.app import get_app_settings


logger = structlog.get_logger()
settings = get_app_settings()
EventType = TypeVar("EventType", bound=InputEvent)


class EmailServiceType(enum.StrEnum):
    welcome = enum.auto()
    weekly_update = enum.auto()
    manager_email = enum.auto()


class IEmailService(ABC, Generic[EventType]):
    @abstractmethod
    def __init__(
        self,
        repository: IRepository,
        user_service: IUserService,
        message_broker_service: IMessageBrokerService,
    ) -> None:
        ...

    @abstractmethod
    async def handle_events(self, event_messages: EventType) -> None:
        ...


class EmailService(IEmailService, Generic[EventType]):
    queue_name: str = settings.notification.email_queue
    collection_name: str = "notifications"
    email_subject: str
    email_from: str
    template_name: str

    def __init__(
        self,
        repository: IRepository,
        user_service: IUserService,
        message_broker_service: IMessageBrokerService,
    ) -> None:
        self.repository = repository
        self.user_service = user_service
        self.message_broker_service = message_broker_service

    def get_template_data(
        self,
        event_msg: EventType,
        user: User,
    ) -> dict[str, Any]:
        raise NotImplementedError(
            "You must implement this method in a subclass",
        )

    def build(self, event_msg: EventType, user: User) -> EmailMessage:
        if not user.email:
            raise ValueError("User has not email")

        template = get_template(template_name=self.template_name)
        template_data = self.get_template_data(event_msg=event_msg, user=user)
        body = template.render(**template_data)

        message = EmailMessage(
            user_id=str(user.id),
            email_from=self.email_from,
            email_to=user.email,
            subject=self.email_subject.format(**template_data),
            body=body,
        )

        return message

    async def transform(self, event: EventType) -> EmailMessage:
        user = await self.user_service.get_users(users_ids=[event.user_id])

        if not user:
            raise ValueError("There is no user with this id")

        return self.build(event_msg=event, user=user[0])

    async def send(self, email: EmailMessage) -> None:
        await asyncio.gather(
            self.repository.insert(
                data=email.model_dump(),
                collection=self.collection_name,
            ),
            self.message_broker_service.publish(
                message_payload=email, queue_name=self.queue_name
            ),
        )

    async def handle_events(self, event_messages: EventType) -> None:
        await logger.info("Message has been consumed from kafka")

        if email := await self.transform(event=event_messages):
            return await self.send(email=email)

        await logger.info("No emails to send")


class WelcomeEmailService(EmailService[InputWelcomeEvent]):
    email_subject = "Welcome to the club!"
    email_from = "cinema-club@cinema.com"
    template_name = "welcome.html"

    def get_template_data(
        self,
        event_msg: InputWelcomeEvent,
        user: User,
    ) -> dict[str, Any]:
        return {"username": user.username}


class WeeklyUpdateEmailService(EmailService[InputWeeklyUpdateEvent]):
    email_subject = "Hi {username}, here is your weekly update!"
    email_from = "cinema-club@cinema.com"
    template_name = "weekly_update.html"

    def get_template_data(
        self,
        event_msg: InputWeeklyUpdateEvent,
        user: User,
    ) -> dict[str, Any]:
        return {
            "username": user.username,
            "watched_films_count": event_msg.watched_films_count,
        }


class ManagerEmailService(IEmailService):
    queue_name: str = settings.notification.email_queue
    collection_name: str = "notifications"

    def __init__(
        self,
        repository: IRepository,
        user_service: IUserService,
        message_broker_service: IMessageBrokerService,
    ) -> None:
        self.repository = repository
        self.user_service = user_service
        self.message_broker_service = message_broker_service

    def build(self, event_msg: InputManagerEvent, user: User) -> EmailMessage:
        if not user.email:
            raise ValueError("User has not email")

        message = EmailMessage(
            user_id=str(user.id),
            email_from=event_msg.email_from,
            email_to=user.email,
            subject=event_msg.subject,
            body=event_msg.body,
        )

        return message

    async def transform(self, event: InputManagerEvent) -> list[EmailMessage]:
        users = await self.user_service.get_users(users_ids=event.users_ids)

        if not users:
            raise ValueError("There is no user with this id")

        return [self.build(event_msg=event, user=user) for user in users]

    async def send_batch(self, emails: list[EmailMessage]) -> None:
        tasks = [
            self.message_broker_service.publish(
                message_payload=email, queue_name=self.queue_name
            )
            for email in emails
        ]

        await asyncio.gather(
            self.repository.insert_many(
                data=[email.model_dump() for email in emails],
                collection=self.collection_name,
            ),
            *tasks,
        )

    async def handle_events(self, event_messages: InputManagerEvent) -> None:
        await logger.info("Message has been consumed from kafka")

        if emails := await self.transform(event=event_messages):
            return await self.send_batch(emails=emails)

        await logger.info("No emails to send")


def email_kafka_service_factory(
    service_schema_type: EmailServiceType
) -> Callable[..., IEmailService]:
    schemas_mapping: dict[EmailServiceType, Type[IEmailService]] = {
        EmailServiceType.welcome: WelcomeEmailService,
        EmailServiceType.weekly_update: WeeklyUpdateEmailService,
        EmailServiceType.manager_email: ManagerEmailService,
    }

    def _service(
        user_service: UserServiceType,
        message_broker_service: MessageBrokerServiceType,
        repository: RepositoryType,
    ) -> IEmailService:
        if service_schema_type in schemas_mapping:
            return schemas_mapping[service_schema_type](
                user_service=user_service,
                message_broker_service=message_broker_service,
                repository=repository,
            )
        raise NotImplementedError

    return _service
