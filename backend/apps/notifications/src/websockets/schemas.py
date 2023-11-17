from pydantic import BaseModel


class WebsocketPush(BaseModel):
    ...


class LikeWebsocketPush(BaseModel):
    user_id: str
