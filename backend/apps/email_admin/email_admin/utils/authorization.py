import http
import time

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import jwt
from pydantic import BaseModel

from email_admin.configs.settings import get_settings

settings = get_settings()


class JwtUserSchema(BaseModel):
    id: str
    permissions: list[str]


class JwtClaims(BaseModel):
    user: JwtUserSchema
    access_jti: str
    refresh_jti: str
    type: str
    exp: int
    iat: int


def decode_token(token: str) -> JwtClaims | None:
    try:
        decoded_token = jwt.decode(
            token,
            settings.auth_jwt_secret_key,
            algorithms=[settings.auth_jwt_encoding_algorithm],
        )
        jwt_claims = JwtClaims(**decoded_token)
        return jwt_claims if jwt_claims.exp >= time.time() else None
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JwtClaims:  # type: ignore
        credentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail="Invalid authorization code.",
            )

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail="Only Bearer token might be accepted",
            )

        decoded_token = decode_token(credentials.credentials)

        if not decoded_token:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail="Invalid or expired token.",
            )

        return decoded_token
