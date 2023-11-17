from uuid import UUID

from pydantic import BaseModel


class InEventSchema(BaseModel):
    user_id: UUID


class InLikeEventSchema(InEventSchema):
    ...
