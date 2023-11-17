from src.common import dependencies as common_deps


class WelcomeEventMessage(common_deps.EventMessage):
    user_id: str


class WeeklyUpdateMessage(common_deps.EventMessage):
    user_id: str
    watched_films_count: int
