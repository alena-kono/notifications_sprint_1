from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from src.common.dependencies import RateLimiterType, UserToken
from src.emails.schemas import EmailMessage
from src.notifications.dependencies import EmailNotificationService


router = APIRouter()


@router.get("/emails", response_model=Page[EmailMessage])
async def get_emails(
    _: RateLimiterType,
    jwt_claims: UserToken,
    service: EmailNotificationService,
    params: Params = Depends(),
) -> Page[EmailMessage]:
    return await service.get_user_emails(
        user_id=jwt_claims.user.id,
        params=params,
    )
