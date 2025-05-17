from pydantic import BaseModel


class SyncCreate(BaseModel):
    text: str
