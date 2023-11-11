from email.message import EmailMessage
from typing import Callable

from jinja2 import Template

from email_worker.configs.jinja2 import get_template
from email_worker.configs.settings import get_settings
from email_worker.email_builders.interface import IEmailBuilder
from email_worker.schemas.events import WelcomeEventSchema
from email_worker.schemas.user import UserSchema


class WelcomeEmailBuilder(IEmailBuilder):
    template_name = "welcome.html"
    email_subject = "Welcome!"

    def __init__(
        self, email_from: str, template_factory: Callable[[str], Template]
    ) -> None:
        self.email_from = email_from
        self.template_factory = template_factory

    def build_message(self, user: UserSchema, event_msg: WelcomeEventSchema) -> str:
        template = self.template_factory(self.template_name)

        data = {"name": user.name}
        output = template.render(**data)

        return output

    def build(
        self,
        event_msg: WelcomeEventSchema,
        user: UserSchema,
    ) -> EmailMessage:
        email_body = self.build_message(user, event_msg)

        message = EmailMessage()
        message["From"] = self.email_from
        message["To"] = user.email
        message["Subject"] = self.email_subject
        message.add_alternative(email_body, subtype="html")

        return message


def get_email_builder() -> WelcomeEmailBuilder:
    settings = get_settings()

    return WelcomeEmailBuilder(
        email_from=settings.email_from,
        template_factory=get_template,
    )
