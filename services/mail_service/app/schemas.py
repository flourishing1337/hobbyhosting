from pydantic import BaseModel, EmailStr


class MailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str
