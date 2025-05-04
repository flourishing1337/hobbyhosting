from fastapi import APIRouter, Depends
from .deps import get_current_user

router = APIRouter()

@router.get("/me")
def read_me(user = Depends(get_current_user)):
    return {"user": user}
