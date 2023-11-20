from typing import Annotated

from fastapi import Depends

from src.notifications.services import NotificationService, email_api_service


EmailNotificationService = Annotated[
    NotificationService,
    Depends(email_api_service),
]
