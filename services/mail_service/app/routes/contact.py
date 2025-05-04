from app.database import contact_messages, database
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str


@router.post("/api/contact")
async def submit_contact(form: ContactForm):
    query = contact_messages.insert().values(
        name=form.name, email=form.email, message=form.message
    )
    await database.execute(query)
    return {"message": "Kontaktmeddelande sparat"}
