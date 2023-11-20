from pydantic import BaseModel


class InputEmailRequest(BaseModel):
    email_to: list[str]
    email_subject: str
    email_body: str


class EmailResponse(BaseModel):
    manager_id: str
    users_ids: list[str]
    email_from: str
    subject: str
    body: str
