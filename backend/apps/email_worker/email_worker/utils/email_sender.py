from abc import ABC, abstractmethod
from email.message import EmailMessage
from types import TracebackType
from typing import Self, Type

from aiosmtplib import SMTP, SMTPException
from faststream import Depends
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_incrementing,
)

from email_worker.configs.smpt import get_smtp_server


class IEmailSender(ABC):
    @abstractmethod
    async def send(self, email_message: EmailMessage) -> None:
        ...

    @abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ) -> None:
        ...


class EmailSender(IEmailSender):
    def __init__(self, smpt_client: SMTP) -> None:
        self.smpt_client = smpt_client

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_incrementing(start=1, increment=5),
        retry=retry_if_exception_type(SMTPException),
    )
    async def _connect(self) -> None:
        await self.smpt_client.connect()

    async def __aenter__(self) -> Self:
        await self._connect()
        return self

    async def __aexit__(
        self,
        exc_type: Type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ) -> None:
        self.smpt_client.close()

    async def send(self, email_message: EmailMessage) -> None:
        from_email = email_message["From"]
        to_emails = email_message["To"].split(",")
        message = email_message.as_string()

        await self.smpt_client.sendmail(from_email, to_emails, message)


def get_email_sender(
    smpt_client: SMTP = Depends(get_smtp_server),
) -> EmailSender:
    return EmailSender(smpt_client)
