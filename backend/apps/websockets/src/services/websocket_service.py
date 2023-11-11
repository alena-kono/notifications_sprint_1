import asyncio
from time import time

from fastapi import Depends, WebSocket, WebSocketDisconnect, WebSocketException
from jose import jwt

from src.configs.settings import Settings, get_settings
from src.queue_router.common import get_router
from src.queue_router.interface import IRouter
from src.schemas.jwt import JwtClaims
from src.services.interfaces import IWebsocketService


class WebSocketMQService(IWebsocketService):
    def __init__(
        self,
        queue_router: IRouter,
        jwt_secret_key: str,
        jwt_encoding_algorithm: str,
    ) -> None:
        self.queue_router = queue_router
        self.jwt_secret_key = jwt_secret_key
        self.jwt_encoding_algorithm = jwt_encoding_algorithm

    def decode_token(self, token: str) -> JwtClaims:
        try:
            decoded_token = jwt.decode(
                token,
                self.jwt_secret_key,
                algorithms=[self.jwt_encoding_algorithm],
            )
            jwt_claims = JwtClaims(**decoded_token)

            if jwt_claims.exp < time():
                raise WebSocketException("Token expired")

            return jwt_claims

        except Exception as e:
            raise WebSocketException("Invalid token") from e

    async def connect(self, websocket: WebSocket, token: str) -> None:
        jwt_claims = self.decode_token(token)

        await websocket.accept()
        self.queue_router.register(jwt_claims.user.id, websocket)

        try:
            while True:
                await asyncio.sleep(1)

        except WebSocketDisconnect:
            await websocket.close()


def get_websocket_service(
    router: IRouter = Depends(get_router),
    settings: Settings = Depends(get_settings),
) -> IWebsocketService:
    return WebSocketMQService(
        queue_router=router,
        jwt_secret_key=settings.jwt_secret_key,
        jwt_encoding_algorithm=settings.jwt_encoding_algorithm,
    )
