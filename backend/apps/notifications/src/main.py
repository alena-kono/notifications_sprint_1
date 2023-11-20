from contextlib import asynccontextmanager
from logging import config as logging_config

import structlog
import uvicorn

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from faststream.rabbit import RabbitBroker
from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis

from src.common import brokers, databases
from src.emails.api.v1.router import router as email_router
from src.notifications.api.v1.routers import router as notifications_router
from src.settings.app import get_app_settings
from src.settings.logging import configure_logger
from src.ws_events.api.v1.router import router as ws_router


settings = get_app_settings()

logging_config.dictConfig(settings.logging.config)
configure_logger(enable_async_logger=True)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    brokers.broker_rabbit = RabbitBroker(
        host=settings.rabbitmq.host,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.username,
        password=settings.rabbitmq.password,
        virtualhost=settings.rabbitmq.vhost,
    )
    await brokers.broker_rabbit.connect()
    await brokers.create_rabbit_queues()
    await brokers.declare_rabbit_exchange()

    databases.redis = aioredis.from_url(settings.redis.dsn, encoding="utf-8")
    databases.mongodb = AsyncIOMotorClient(settings.mongo.dsn)
    await FastAPILimiter.init(databases.redis)

    ws_lf = ws_router.lifespan_context
    email_lf = email_router.lifespan_context
    async with ws_lf(app), email_lf(app):
        yield

    await ws_router.shutdown()
    await email_router.shutdown()
    if brokers.broker_kafka is not None:
        await brokers.broker_kafka.close()
    if brokers.broker_rabbit is not None:
        await brokers.broker_rabbit.close()
    if databases.mongodb is not None:
        databases.mongodb.close()
    if databases.redis is not None:
        await databases.redis.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.service.name,
    description=settings.service.description,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    version="0.1.0",
)


app.include_router(email_router, tags=["email-kafka"])
app.include_router(ws_router, tags=["ws-kafka"])
app.include_router(
    prefix="/api/v1/notifications",
    router=notifications_router,
    tags=["notifications-kafka"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.service.host,
        port=settings.service.port,
        reload=settings.service.debug,
    )
