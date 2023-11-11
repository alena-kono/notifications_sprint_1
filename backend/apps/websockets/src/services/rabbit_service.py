import asyncio

from fastapi import Depends

from src.queue_router.common import get_router
from src.queue_router.interface import IRouter
from src.schemas.in_events import InLikeEventSchema
from src.schemas.out_events import OutLikeEventSchema
from src.services.interfaces import IRabbitMQService


# TODO: Make it Generic
class RabbitMQService(IRabbitMQService):
    def __init__(self, queue_router: IRouter) -> None:
        self.queue_router = queue_router

    async def handle_event(self, event: InLikeEventSchema) -> None:
        user_id = event.user_id
        out_event = OutLikeEventSchema(user_id=user_id).model_dump_json()

        websockets = await self.queue_router.get(event.user_id)
        if not websockets:
            # In case when we have several workers, it is possible that
            # the user is not connected to the current websocket
            # server, so we can just ignore the event
            return None
        print(websockets)
        tasks = [websocket.send_json(out_event) for websocket in websockets]
        await asyncio.gather(*tasks)


def get_rabbitmq_service(
    router: IRouter = Depends(get_router),
) -> IRabbitMQService:
    return RabbitMQService(queue_router=router)
