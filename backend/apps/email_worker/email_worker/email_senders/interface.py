from abc import ABC, abstractmethod
from email.message import EmailMessage


class IEmailSender(ABC):
    @abstractmethod
    async def send(self, email_message: EmailMessage) -> None:
        ...
