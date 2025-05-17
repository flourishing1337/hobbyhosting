from datetime import datetime

from admin_sync_service.app.dependencies import Base
from sqlalchemy import Column, DateTime, Integer, String


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
