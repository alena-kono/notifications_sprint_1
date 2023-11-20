from pydantic import BaseModel, EmailStr


class InputEvent(BaseModel):
    user_id: str


class InputWelcomeEvent(InputEvent):
    ...


class InputWeeklyUpdateEvent(InputEvent):
    watched_films_count: int


class InputManagerEvent(BaseModel):
    email_from: EmailStr
    users_ids: list[str]
    subject: str
    body: str


class EmailMessage(BaseModel):
    user_id: str
    email_from: EmailStr = "welcome@cinema-club.com"
    email_to: EmailStr
    subject: str
    body: str
