import asyncio

from fastapi_pagination import Page, Params

from src.common.dependencies import RepositoryType
from src.common.repositories import IRepository
from src.emails.schemas import EmailMessage


class NotificationService:
    collection_name: str = "notifications"

    def __init__(self, repository: IRepository) -> None:
        self.repository = repository

    async def get_user_emails(
        self,
        user_id: str,
        params: Params,
    ) -> Page[EmailMessage]:
        skip = (params.page - 1) * params.size

        emails, count = await asyncio.gather(
            self.repository.get_list(
                filters={"user_id": user_id},
                skip=skip,
                limit=params.size,
                collection=self.collection_name,
            ),
            self.repository.count(
                filters={"user_id": user_id},
                collection=self.collection_name,
            ),
        )
        return Page.create(items=emails, params=params, total=count)

    async def get_user_events(
        self,
        user_id: str,
        params: Params,
    ) -> None:
        ...


def email_api_service(repository: RepositoryType) -> NotificationService:
    return NotificationService(repository=repository)
