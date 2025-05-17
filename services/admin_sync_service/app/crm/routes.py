from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# 📁 apps/admin_sync_service/app/crm/routes.py
from ..dependencies import get_db
from . import models, schemas

router = APIRouter(prefix="/crm", tags=["CRM"])


@router.post("/companies", response_model=schemas.CompanyOut)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(
        name=company.name,
        status=company.status,
        notes=company.notes,
    )
    db.add(db_company)
    db.flush()  # to generate db_company.id

    for contact in company.contacts:
        db_contact = models.Contact(**contact.dict(), company_id=db_company.id)
        db.add(db_contact)

    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/companies", response_model=List[schemas.CompanyOut])
def list_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()


@router.get("/companies/{company_id}", response_model=schemas.CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/companies/{company_id}/todos", response_model=schemas.ToDoOut)
def create_todo(
    company_id: int, todo: schemas.ToDoCreate, db: Session = Depends(get_db)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db_todo = models.ToDo(**todo.dict(), company_id=company_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/companies/{company_id}/todos", response_model=List[schemas.ToDoOut])
def list_todos(company_id: int, db: Session = Depends(get_db)):
    return db.query(models.ToDo).filter(models.ToDo.company_id == company_id).all()


@router.get("/todos/{todo_id}", response_model=schemas.ToDoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="To-do not found")
    return todo


@router.put("/todos/{todo_id}", response_model=schemas.ToDoOut)
def update_todo(todo_id: int, todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="To-do not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="To-do not found")
    db.delete(db_todo)
    db.commit()
    return None
