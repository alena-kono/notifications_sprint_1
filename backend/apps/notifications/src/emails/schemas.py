from abc import ABC, abstractmethod
from typing import TypeVar, Self

from pydantic import BaseModel

from src.common import schemas as common_schemas
from src.emails import dependencies as emails_deps


class WelcomeContent(BaseModel):
    username: str


class WeeklyUpdateContent(BaseModel):
    username: str

    likes_count: int
    comments_count: int
    watched_films_count: int


class IEmail(BaseModel, ABC):
    email_to: str
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
                    likes_count=event_message.likes_count,
                    comments_count=event_message.comments_count,
                    watched_films_count=event_message.watched_films_count,
                ),
            )
        raise TypeError(
            f"`event_message` arg has incorrect type, should be {type(cls)}"
        )


EmailType = TypeVar("EmailType", bound=IEmail)
EmailContentType = TypeVar("EmailContentType", bound=BaseModel)
