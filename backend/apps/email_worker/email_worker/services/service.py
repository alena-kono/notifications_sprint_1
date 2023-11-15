import asyncio
from abc import ABC, abstractmethod
from email.message import EmailMessage
from enum import StrEnum
from typing import Callable

from aiosmtplib import SMTPException
from faststream import Depends
from jinja2 import Template
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_incrementing,
)

from email_worker.configs.jinja2 import get_template
from email_worker.schemas.events import EventSchema
from email_worker.utils.email_sender import IEmailSender, get_email_sender


class ServiceType(StrEnum):
    WELCOME = "welcome"
    WEEKLY_UPDATE = "weekly-update"


class IService(ABC):
    @abstractmethod
    async def handle_event(self, event_msg: list[EventSchema]) -> None:
        ...


class Service(IService):
    def __init__(
        self, subject: str, template: Template, email_sender: IEmailSender
    ) -> None:
        self.subject = subject
        self.template = template
        self.email_sender = email_sender

    def build(self, event_msg: EventSchema) -> EmailMessage:
        data = event_msg.content.model_dump()

        subject = self.subject.format(**data)
        email_body = self.template.render(**data)

        message = EmailMessage()
        message["From"] = event_msg.email_from
        message["To"] = event_msg.email_to
        message["Subject"] = subject
        message.add_alternative(email_body, subtype="html")

        return message

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_incrementing(start=1, increment=5),
        retry=retry_if_exception_type(SMTPException),
    )
    async def send_batch(self, emails: list[EmailMessage]) -> None:
        print("Sending batch of emails")
        async with self.email_sender as email_sender:
            tasks = [email_sender.send(email) for email in emails]
            await asyncio.gather(*tasks)

    async def handle_event(self, event_msg: list[EventSchema]) -> None:
        emails = [self.build(event) for event in event_msg]
        await self.send_batch(emails)


def service_factory(
    service_type: ServiceType,
) -> Callable[[IEmailSender], Service]:
    template_map: dict[ServiceType, dict[str, str]] = {
        ServiceType.WELCOME: {
            "template": "welcome.html",
            "subject": "Welcome to the club!",
        },
        ServiceType.WEEKLY_UPDATE: {
            "template": "weekly_update.html",
            "subject": "Hi {username}, here is your weekly update!",
        },
    }

    def _service(
        email_sender: IEmailSender = Depends(get_email_sender),
    ) -> Service:
        template = get_template(template_map[service_type]["template"])
        subject_template = template_map[service_type]["subject"]
        return Service(
            email_sender=email_sender,
            template=template,
            subject=subject_template,
        )

    return _service
