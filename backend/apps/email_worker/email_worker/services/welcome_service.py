from faststream import Depends

from email_worker.email_builders.interface import IEmailBuilder
from email_worker.email_builders.welcome_builder import get_email_builder
from email_worker.email_senders.interface import IEmailSender
from email_worker.email_senders.sender import get_email_sender
from email_worker.schemas.events import WelcomeEventSchema
from email_worker.services.common import Service


class WelcomeService(Service[WelcomeEventSchema]):
    ...


def get_welcome_service(
    email_sender: IEmailSender = Depends(get_email_sender),
    email_builder: IEmailBuilder = Depends(get_email_builder),
) -> WelcomeService:
    return WelcomeService(
        email_sender=email_sender,
        email_builder=email_builder,
    )
