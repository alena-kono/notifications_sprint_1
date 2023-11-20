from typing import Annotated

from fastapi import Depends

from src.emails.schemas import (
    InputManagerEvent,
    InputWeeklyUpdateEvent,
    InputWelcomeEvent,
)
from src.emails.services import (
    EmailServiceType,
    IEmailService,
    email_kafka_service_factory,
)


WelcomeEmailService = Annotated[
    IEmailService[InputWelcomeEvent],
    Depends(email_kafka_service_factory(EmailServiceType.welcome)),
]

WeeklyUpdateEmailService = Annotated[
    IEmailService[InputWeeklyUpdateEvent],
    Depends(email_kafka_service_factory(EmailServiceType.weekly_update)),
]

ManagerEmailService = Annotated[
    IEmailService[InputManagerEvent],
    Depends(email_kafka_service_factory(EmailServiceType.manager_email)),
]
