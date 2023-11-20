from pydantic import BaseModel, EmailStr


class EmailEvent(BaseModel):
    user_id: str
    email_from: EmailStr
    email_to: EmailStr
    subject: str
    body: str
