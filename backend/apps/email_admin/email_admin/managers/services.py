import asyncio
from uuid import UUID

from fastapi_pagination import Page, Params

from email_admin.configs.settings import get_settings
from email_admin.managers.schemas import EmailResponse, InputEmailRequest
from email_admin.utils.dependencies import MessageQueueType, RepositoryType
from email_admin.utils.message_queue import IMessageQueue
from email_admin.utils.repositories import IRepository

settings = get_settings()


class EmailAdminService:
    kafka_topic = settings.kafka_topic
    collection = "manager_emails"

    def __init__(self, message_queue: IMessageQueue, repository: IRepository):
        self.message_queue = message_queue
        self.repository = repository

    def get_manager_emails(self, user_id: UUID) -> str:
        return "manager@cinema.com"

    async def send_email(self, email: EmailResponse) -> None:
        await self.message_queue.push(
            topic=self.kafka_topic,
            message=email.model_dump_json(exclude={"user_id"}).encode(),
        )
        await self.repository.insert(
            data=email.model_dump(),
            collection=self.collection,
        )

    async def create_email(
        self, email: InputEmailRequest, user_id: str
    ) -> EmailResponse:
        manager_email = self.get_manager_emails(user_id=user_id)

        email_response = EmailResponse(
            manager_id=user_id,
            body=email.email_body,
            email_from=manager_email,
            subject=email.email_subject,
            users_ids=email.email_to,
        )
        await self.send_email(email=email_response)
        return email_response

    async def get_emails(
        self,
        user_id: str,
        params: Params,
    ) -> Page[EmailResponse]:
        emails, total = await asyncio.gather(
            self.repository.get_list(
                collection=self.collection,
                filters={"manager_id": str(user_id)},
            ),
            self.repository.count(
                collection=self.collection,
                filters={"manager_id": str(user_id)},
            ),
        )
        return Page.create(items=emails, params=params, total=total)


def get_email_admin_service(
    message_queue: MessageQueueType,
    repository: RepositoryType,
) -> EmailAdminService:
    return EmailAdminService(
        message_queue=message_queue,
        repository=repository,
    )
