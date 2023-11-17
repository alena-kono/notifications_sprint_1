from collections import defaultdict
from functools import lru_cache
from uuid import UUID

from fastapi import WebSocket

from src.queue_router.interface import IRouter


class Router(IRouter):
    def __init__(self) -> None:
        self.mapping: dict[UUID, list[WebSocket]] = defaultdict(list)

    def register(self, id_: UUID, websocket: WebSocket) -> None:
        self.mapping[id_].append(websocket)

    async def get(self, id_: UUID) -> list[WebSocket]:
        return self.mapping[id_]


@lru_cache(maxsize=1)
def get_router() -> IRouter:
    return Router()
