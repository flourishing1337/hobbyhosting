from datetime import datetime

from app.dependencies import Base
from sqlalchemy import Column, DateTime, Integer, String


class Sync(Base):
    __tablename__ = "syncs"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
