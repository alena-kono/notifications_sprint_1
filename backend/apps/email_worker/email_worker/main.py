import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from email_worker.api.v1.api import router
from email_worker.configs.settings import get_settings

broker = RabbitBroker()
app = FastStream(broker=broker)


@app.on_startup
async def on_startup() -> None:
    settings = get_settings()

    await broker.connect(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_username,
        password=settings.rabbitmq_password,
        virtualhost=settings.rabbitmq_vhost,
    )


@app.on_shutdown
async def on_shutdown() -> None:
    ...





broker.include_router(router)

if __name__ == "__main__":
    asyncio.run(app.run())
