from abc import ABC, abstractmethod
from typing import TypeVar, Self

from pydantic import BaseModel, EmailStr

from src.common import schemas as common_schemas
from src.emails import dependencies as emails_deps


class WelcomeContent(BaseModel):
    username: str


class WeeklyUpdateContent(BaseModel):
    username: str
    watched_films_count: int


class IEmail(BaseModel, ABC):
    email_to: EmailStr
    email_from: EmailStr
    content: dict

    @classmethod
    @abstractmethod
    def create(
        cls,
        user: common_schemas.User,
        event_message: emails_deps.EventMessageType | None,
    ) -> Self:
        raise NotImplementedError


class WelcomeEmail(IEmail):
    email_from: EmailStr = "welcome@cinema-club.com"
    content: WelcomeContent

    @classmethod
    def create(
        cls,
        user: common_schemas.User,
        event_message: emails_deps.EventMessageType | None = None,
    ) -> Self:
        return cls(
            email_to=user.email,
            content=WelcomeContent(username=user.username),
        )


class WeeklyUpdateEmail(IEmail):
    email_from: EmailStr = "no-reply@cinema-club.com"
    content: WeeklyUpdateContent

    @classmethod
    def create(
        cls,
        user: common_schemas.User,
        event_message: emails_deps.WeeklyUpdateMessage | None,
    ) -> Self:
        if isinstance(event_message, emails_deps.WeeklyUpdateMessage):
            return cls(
                email_to=user.email,
                content=WeeklyUpdateContent(
                    username=user.username,
                    watched_films_count=event_message.watched_films_count,
                ),
            )
        raise TypeError(
            f"`event_message` arg has incorrect type, should be {type(cls)}"
        )


EmailType = TypeVar("EmailType", bound=IEmail)
EmailContentType = TypeVar("EmailContentType", bound=BaseModel)
