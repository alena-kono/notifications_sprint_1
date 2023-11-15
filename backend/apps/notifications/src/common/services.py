from abc import ABC, abstractmethod
import structlog

from src.common import schemas as common_schemas

logger = structlog.get_logger()


class IUserService(ABC):
    @abstractmethod
    async def get_users(self, users_ids: list[str]) -> list[common_schemas.User]:
        ...


class UserService:
    users_storage_mock = {
        "1": {
            "username": "Eugenia",
            "email": "eugenia@gmail.com",
        },
        "2": {
            "username": "jack",
            "email": "jack@mail.com",
        },
    }

    async def get_users(self, users_ids: list[str]) -> list[common_schemas.User]:
        # TODO: Check if user exists
        # TODO: Get user data from user-account-service
        # TODO: Check if user wants to receive the notification
        fetched_users = []
        for id_ in users_ids:
            if user := self.users_storage_mock.get(id_):
                fetched_users.append(common_schemas.User(id=id_, **user))
        return fetched_users


class INotificationService(ABC):
    @abstractmethod
    async def handle_event(self, event):
        ...

    @abstractmethod
    async def _get_users(self, users_id: list[str]) -> list[common_schemas.User]:
        ...


class NotificationService:
    def __init__(self, user_service: IUserService) -> None:
        self.user_service = user_service

    async def handle_event(self, event):
        ...

    async def _get_users(self, users_ids: list[str]) -> list[common_schemas.User]:
        return await self.user_service.get_users(users_ids=users_ids)


def get_user_service() -> IUserService:
    return UserService()
