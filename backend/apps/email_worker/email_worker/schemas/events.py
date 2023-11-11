from uuid import UUID

from pydantic import BaseModel


class EventSchema(BaseModel):
    user_id: UUID


class WelcomeEventSchema(EventSchema):
    ...
