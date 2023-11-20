from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from email_admin.configs import kafka, mongo
from email_admin.configs.settings import get_settings
from email_admin.managers.api.v1.routers import router as manager_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
        compression_type="gzip",
        enable_idempotence=True,
        max_batch_size=32768,
        linger_ms=1000,
        request_timeout_ms=10000,
        retry_backoff_ms=1000,
    )
    await kafka.producer.start()
    mongo.mongodb = AsyncIOMotorClient(
        f"{settings.mongo_host}:{settings.mongo_port}",
    )

    yield

    if mongo.mongodb is not None:
        mongo.mongodb.close()

    if kafka.producer is not None:
        await kafka.producer.stop()


app = FastAPI(
    lifespan=lifespan,
    title=settings.service_name,
    description=settings.service_description,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    version="0.1.0",
)

app.include_router(router=manager_router, prefix="/api/v1", tags=["manager"])


@app.get("/ping")
def pong() -> dict[str, str]:
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(
        "email_admin.main:app",
        host=settings.service_host,
        port=settings.service_port,
    )
