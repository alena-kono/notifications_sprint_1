from uuid import UUID

from pydantic import BaseModel


class JwtUserSchema(BaseModel):
    id: UUID
    permissions: list[str]


class JwtClaims(BaseModel):
    user: JwtUserSchema
    access_jti: str
    refresh_jti: str
    type: str
    exp: int
    iat: int
