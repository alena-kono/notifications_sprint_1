from uuid import UUID

from pydantic import BaseModel


class OutEventSchema(BaseModel):
    user_id: UUID


class OutLikeEventSchema(OutEventSchema):
    ...
