from src.common import dependencies as common_deps


class LikeEventMessage(common_deps.EventMessage):
    user_id: str
