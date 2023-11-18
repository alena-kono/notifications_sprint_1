from ipaddress import IPv4Address
from uuid import UUID

from pydantic import EmailStr
from src.common import schemas as common_schemas


class User(common_schemas.UUIDSchemaMixin):
    username: str
    first_name: str
    last_name: str
    permissions: list[str]
    email: EmailStr | None = None


class UserLoginRecord(
    common_schemas.UUIDSchemaMixin,
    common_schemas.TimestampSchemaMixin,
):
    user_id: UUID
    user_agent: str
    ip_address: IPv4Address
