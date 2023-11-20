from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class EventMessage(BaseModel):
    ...


class User(BaseModel):
    id: UUID
    username: str
    email: EmailStr | None = None


class AccessToken(BaseModel):
    access_token: str = Field(pattern=r"^(?:[\w-]*\.){2}[\w-]*$")


class RefreshToken(BaseModel):
    refresh_token: str = Field(pattern=r"^(?:[\w-]*\.){2}[\w-]*$")


class JWTCredentials(RefreshToken, AccessToken):
    ...


class User(BaseModel):
    id: str
    username: str
    email: str
