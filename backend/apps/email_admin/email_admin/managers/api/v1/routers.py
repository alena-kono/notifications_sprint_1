from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params

from email_admin.managers.dependencies import EmailAdminServiceType
from email_admin.managers.schemas import EmailResponse, InputEmailRequest
from email_admin.utils.dependencies import UserToken

router = APIRouter()


@router.get("/emails", response_model=Page[EmailResponse])
async def get_emails(
    jwt_claims: UserToken,
    service: EmailAdminServiceType,
    params: Params = Depends(),
) -> Page[EmailResponse]:
    return await service.get_emails(
        user_id=jwt_claims.user.id,
        params=params,
    )


@router.post("/emails", response_model=EmailResponse)
async def create_email(
    jwt_claims: UserToken,
    service: EmailAdminServiceType,
    email: InputEmailRequest,
) -> EmailResponse:
    return await service.create_email(
        email=email,
        user_id=jwt_claims.user.id,
    )
