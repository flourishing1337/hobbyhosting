from datetime import datetime

from admin_sync_service.app.dependencies import Base
from sqlalchemy import Column, DateTime, Integer, String


class AdminFile(Base):
    __tablename__ = "admin_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
