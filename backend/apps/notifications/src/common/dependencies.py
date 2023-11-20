from typing import Annotated

from fastapi import Depends
from fastapi_limiter.depends import RateLimiter
from motor.core import AgnosticClient

from src.common.authorization import JWTBearer, JwtClaims
from src.common.databases import get_mongodb
from src.common.repositories import IRepository, MongoRepository
from src.common.services import (
    IMessageBrokerService,
    IUserService,
    get_message_broker_service,
    get_user_service,
)
from src.settings.app import get_app_settings


settings = get_app_settings()


MessageBrokerServiceType = Annotated[
    IMessageBrokerService,
    Depends(get_message_broker_service),
]
UserServiceType = Annotated[IUserService, Depends(get_user_service)]
MongoCLientType = Annotated[AgnosticClient, Depends(get_mongodb)]


def get_repository(mongo_client: MongoCLientType) -> IRepository:
    return MongoRepository(
        mongo_client=mongo_client,
        db_name=settings.mongo.db_name,
    )


UserToken = Annotated[JwtClaims, Depends(JWTBearer())]
RepositoryType = Annotated[IRepository, Depends(get_repository)]
RateLimiterType = Annotated[
    RateLimiter,
    Depends(
        RateLimiter(
            times=settings.rate_limiter.STANDARD_LIMIT.times,
            seconds=settings.rate_limiter.STANDARD_LIMIT.seconds,
        )
    ),
]
