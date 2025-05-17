from app.dependencies import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    notes = Column(Text)

    contacts = relationship(
        "Contact", back_populates="company", cascade="all, delete-orphan"
    )
    todos = relationship("ToDo", back_populates="company", cascade="all, delete-orphan")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)

    company = relationship("Company", back_populates="contacts")


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    company = relationship("Company", back_populates="todos")
