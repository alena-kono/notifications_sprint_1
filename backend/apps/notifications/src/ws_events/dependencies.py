from typing import Annotated

from fastapi import Depends

from src.ws_events.services import (
    WebsocketService,
    WebsocketServiceType,
    ws_service_factory,
)


LikeWebsocketServiceType = Annotated[
    WebsocketService,
    Depends(ws_service_factory(WebsocketServiceType.like)),
]
