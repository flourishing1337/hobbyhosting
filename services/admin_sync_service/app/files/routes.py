import os

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..main import verify_token
from . import models, schemas

UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR", os.path.join(os.path.dirname(__file__), "../../uploads")
)
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("", response_model=schemas.FileOut)
async def upload_file(
    upload_file: UploadFile = File(...),
    username: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    file_location = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_location, "wb") as f:
        content = await upload_file.read()
        f.write(content)
    db_file = models.AdminFile(
        filename=upload_file.filename,
        filepath=file_location,
        uploaded_by=username,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


@router.get("", response_model=list[schemas.FileOut])
async def list_files(
    username: str = Depends(verify_token), db: Session = Depends(get_db)
):
    return db.query(models.AdminFile).all()


@router.get("/{file_id}/download")
async def download_file(
    file_id: int, username: str = Depends(verify_token), db: Session = Depends(get_db)
):
    db_file = db.query(models.AdminFile).filter(models.AdminFile.id == file_id).first()
    if not db_file:
        return FileResponse(path=None, status_code=404)
    return FileResponse(path=db_file.filepath, filename=db_file.filename)
