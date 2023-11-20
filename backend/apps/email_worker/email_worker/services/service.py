from abc import ABC, abstractmethod
from email.message import EmailMessage

from aiosmtplib import SMTPException
from faststream import Depends
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_incrementing,
)

from email_worker.schemas.events import EmailEvent
from email_worker.utils.email_sender import IEmailSender, get_email_sender


class IService(ABC):
    @abstractmethod
    async def handle_event(self, event_msg: EmailEvent) -> None:
        ...


class Service(IService):
    def __init__(self, email_sender: IEmailSender) -> None:
        self.email_sender = email_sender

    def build(self, event_msg: EmailEvent) -> EmailMessage:
        message = EmailMessage()
        message["From"] = event_msg.email_from
        message["To"] = event_msg.email_to
        message["Subject"] = event_msg.subject
        message.add_alternative(event_msg.body, subtype="html")

        return message

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_incrementing(start=1, increment=5),
        retry=retry_if_exception_type(SMTPException),
    )
    async def send(self, email: EmailMessage) -> None:
        async with self.email_sender as email_sender:
            await email_sender.send(email)

    async def handle_event(self, event_msg: EmailEvent) -> None:
        email = self.build(event_msg)
        await self.send(email)


def service(
    email_sender: IEmailSender = Depends(get_email_sender),
) -> Service:
    return Service(email_sender=email_sender)
