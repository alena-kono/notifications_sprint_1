from typing import Generic, TypeVar

from pydantic import BaseModel

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class EventSchema(BaseModel, Generic[SchemaType]):
    email_from: str
    email_to: str
    email_subject: str
    content: SchemaType


class WelcomeContentSchema(BaseModel):
    username: str


class WeeklyUpdateContentSchema(BaseModel):
    username: str

    likes_count: int
    comments_count: int
    watched_films_count: int