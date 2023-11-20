import httpx

from fastapi import Depends
from pydantic import HttpUrl

from src.common.schemas import AccessToken
from src.settings.app import AppSettings, get_app_settings


class APIClient:
    def __init__(self, base_url: HttpUrl, access_jwt: AccessToken) -> None:
        self.base_url = base_url
        self.access_jwt = access_jwt

    async def get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=url,
                headers={
                    "Authorization": f"Bearer {self.access_jwt.access_token}",
                },
            )
        response.raise_for_status()

        return response.json()


def get_api_client(
    settings: AppSettings = Depends(get_app_settings),
) -> APIClient:
    return APIClient(
        base_url=settings.integration.auth_users_url,
        access_jwt=AccessToken(
            access_token=settings.integration.auth_access_jwt,
        ),
    )
