from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True


class ToDoBase(BaseModel):
    title: str
    due_date: Optional[date] = None
    completed: bool = False


class ToDoCreate(ToDoBase):
    pass


class ToDoOut(ToDoBase):
    id: int

    class Config:
        from_attributes = True


class CompanyBase(BaseModel):
    name: str
    status: str
    notes: Optional[str] = None


class CompanyCreate(CompanyBase):
    contacts: List[ContactCreate] = []


class CompanyOut(CompanyBase):
    id: int
    contacts: List[ContactOut] = []
    todos: List[ToDoOut] = []

    class Config:
        from_attributes = True
