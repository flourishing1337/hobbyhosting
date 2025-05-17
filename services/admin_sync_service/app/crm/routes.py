from typing import List

# 📁 apps/admin_sync_service/app/crm/routes.py
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
