from pydantic import BaseModel


class InputLikeEvent(BaseModel):
    user_id: str


class WebsocketPush(BaseModel):
    user_id: str


class LikeWebsocketPush(WebsocketPush):
    ...
