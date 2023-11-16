from typing import Generic, TypeVar

from pydantic import BaseModel

EventMessageType = TypeVar("EventMessageType", bound=BaseModel)


class WelcomeEventMessage(BaseModel, Generic[EventMessageType]):
    user_id: str


class WeeklyUpdateMessage(BaseModel, Generic[EventMessageType]):
    user_id: str
    watched_films_count: int
