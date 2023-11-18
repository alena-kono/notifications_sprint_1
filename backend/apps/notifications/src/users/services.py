from abc import ABC, abstractmethod

from faststream import Depends

from src.common import schemas as common_schemas
from src.integrations.common.client import APIClient, get_api_client
from src.users import schemas as users_schemas


class IUserService(ABC):
    @abstractmethod
    async def get_users(self, users_ids: list[str]) -> list[common_schemas.User]:
        ...


class UserService(IUserService):
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client

    async def get_users(self, users_ids: list[str]) -> list[users_schemas.User]:
        ids_query = "&".join([f"ids={user_id}" for user_id in users_ids])

        response_data = await self.api_client.get(path=f"?{ids_query}")

        return [users_schemas.User(**user) for user in response_data]


def get_user_service(api_client: APIClient = Depends(get_api_client)) -> IUserService:
    return UserService(api_client=api_client)
