from fastapi import APIRouter, Depends, Query, WebSocket
from src.services.interfaces import IWebsocketService
from src.services.websocket_service import get_websocket_service

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(),
    service: IWebsocketService = Depends(get_websocket_service),
):
    await service.connect(websocket, token)
