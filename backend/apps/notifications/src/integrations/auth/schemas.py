from pydantic import BaseModel, Field


class AccessToken(BaseModel):
    access_token: str = Field(pattern=r"^(?:[\w-]*\.){2}[\w-]*$")


class RefreshToken(BaseModel):
    refresh_token: str = Field(pattern=r"^(?:[\w-]*\.){2}[\w-]*$")


class JWTCredentials(RefreshToken, AccessToken):
    ...
