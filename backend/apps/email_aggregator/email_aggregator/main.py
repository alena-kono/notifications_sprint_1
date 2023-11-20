import uvicorn
from fastapi import FastAPI

from email_aggregator.settings.app import get_app_settings

settings = get_app_settings()

API_VERSION = "v1"

API_PREFIX = f"/api/{API_VERSION}"

app = FastAPI(
    title="email_aggregator",
    description="Email aggregator",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    version="0.1.0",
)


@app.get(f"{API_PREFIX}/ping")
def pong() -> dict[str, str]:
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(
        "email_aggregator.main:app",
        host=settings.service.host,
        port=settings.service.port,
    )
