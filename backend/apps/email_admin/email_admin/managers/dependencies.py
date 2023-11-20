from typing import Annotated

from fastapi import Depends

from email_admin.managers.services import EmailAdminService, get_email_admin_service

EmailAdminServiceType = Annotated[
    EmailAdminService,
    Depends(get_email_admin_service),
]
