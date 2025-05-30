from datetime import datetime

from pydantic import BaseModel


class FileOut(BaseModel):
    id: int
    filename: str
    uploaded_by: str
    created_at: datetime

    class Config:
        from_attributes = True
