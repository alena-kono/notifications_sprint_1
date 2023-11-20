from typing import Annotated

from fastapi import Depends

from src.emails.schemas import (
    InputManagerEvent,
    InputWeeklyUpdateEvent,
    InputWelcomeEvent,
)
from src.emails.services import (
    EmailService,
    EmailServiceType,
    email_kafka_service_factory,
)


WelcomeEmailService = Annotated[
    EmailService[InputWelcomeEvent],
    Depends(email_kafka_service_factory(EmailServiceType.welcome)),
]

WeeklyUpdateEmailService = Annotated[
    EmailService[InputWeeklyUpdateEvent],
    Depends(email_kafka_service_factory(EmailServiceType.weekly_update)),
]

ManagerEmailService = Annotated[
    EmailService[InputManagerEvent],
    Depends(email_kafka_service_factory(EmailServiceType.manager_email)),
]
