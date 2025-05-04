from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import UserCreate, TokenOut
from .models import User, Base
from .dependencies import get_db, engine
from .hashing import hash_password, verify_password
from .jwt_utils import create_token

# ------------- init -------------
Base.metadata.create_all(bind=engine)   # auto-skapa tabeller om de saknas

app = FastAPI(title="Auth Service")

# ----------- endpoints -----------

@app.get("/auth/health")
def health():
    return {"status": "ok"}

@app.post("/auth/login", response_model=TokenOut)
def login(form: UserCreate, db: Session = Depends(get_db)):
    user: User | None = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    return {"access_token": create_token(user.username)}

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        hashed_pw=hash_password(user.password),
        is_admin=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "message": "Admin user created 🎉"}
