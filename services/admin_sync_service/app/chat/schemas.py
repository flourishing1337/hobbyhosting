from datetime import datetime

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    message: str


class ChatMessageOut(ChatMessageCreate):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
