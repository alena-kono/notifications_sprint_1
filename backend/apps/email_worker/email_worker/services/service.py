import asyncio
from abc import ABC, abstractmethod
from email.message import EmailMessage
from enum import StrEnum
from typing import Callable

from faststream import Depends
from jinja2 import Template

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
    def __init__(self, template: Template, email_sender: IEmailSender) -> None:
        self.template = template
        self.email_sender = email_sender

    def build(self, event_msg: EventSchema) -> EmailMessage:
        data = event_msg.content.model_dump()
        email_body = self.template.render(**data)

        message = EmailMessage()
        message["From"] = event_msg.email_from
        message["To"] = event_msg.email_to
        message["Subject"] = event_msg.email_subject
        message.add_alternative(email_body, subtype="html")

        return message

    async def handle_event(self, event_msg: list[EventSchema]) -> None:
        emails = [self.build(event) for event in event_msg]

        async with self.email_sender as email_sender:
            tasks = [email_sender.send(email) for email in emails]
            asyncio.gather(*tasks)


def service_factory(
    service_type: ServiceType,
) -> Callable[[IEmailSender], Service]:
    template_map: dict[ServiceType, str] = {
        ServiceType.WELCOME: "welcome.html",
        ServiceType.WEEKLY_UPDATE: "weekly_update.html",
    }

    def _service(
        email_sender: IEmailSender = Depends(get_email_sender),
    ) -> Service:
        template = get_template(template_map[service_type])
        return Service(email_sender=email_sender, template=template)

    return _service
