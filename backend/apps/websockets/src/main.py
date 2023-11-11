from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.v1.rabbit import rabbit_router
from src.api.v1.websockets import router as websockets_router
from src.configs.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.service_name,
    description=settings.service_description,
    version=settings.service_version,
    debug=settings.service_debug,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    lifespan=rabbit_router.lifespan_context,
)

app.include_router(rabbit_router, tags=["rabbitmq"])
app.include_router(websockets_router, tags=["websockets"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.service_host,
        port=settings.service_port,
        reload=settings.service_debug,
    )
