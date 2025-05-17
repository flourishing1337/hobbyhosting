# 📁 apps/admin_sync_service/app/main.py
from datetime import datetime, timedelta

from admin_sync_service.app.crm.routes import router as crm_router
from admin_sync_service.app.dependencies import Base, engine, get_db
from admin_sync_service.app.sync.models import Sync
from admin_sync_service.app.sync.schemas import (  # Flytta gärna till app/sync/schemas.py
    SyncCreate,
)
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS settings
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://sync.hobbyhosting.org",
    "https://admin.hobbyhosting.org",
    "https://hobbyhosting.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


# Middleware to allow credentials and methods
async def add_response_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


app.middleware("http")(add_response_headers)


@app.options("/{rest_of_path:path}")
async def options_handler(rest_of_path: str):
    return JSONResponse(
        content={},
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Auth verification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        print(f"Verifying token: {token[:20]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")

        username = payload.get("sub")
        is_admin = payload.get("is_admin", False)

        print(f"Username: {username}, Is Admin: {is_admin}")
        if not username:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        if not is_admin:
            raise HTTPException(status_code=403, detail="User is not an admin")

        return username
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Existing endpoints
@app.get("/users/online")
async def get_online_users(
    username: str = Depends(verify_token), db: Session = Depends(get_db)
):
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    online_users = (
        db.query(Sync.username)
        .distinct()
        .filter(Sync.created_at >= five_minutes_ago)
        .all()
    )
    return [{"username": user.username} for user in online_users]


@app.post("/messages")
async def create_sync(
    sync: SyncCreate,
    username: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    db_sync = Sync(text=sync.text, username=username)
    db.add(db_sync)
    db.commit()
    db.refresh(db_sync)
    return db_sync


@app.get("/messages")
async def get_syncs(
    username: str = Depends(verify_token), db: Session = Depends(get_db)
):
    syncs = db.query(Sync).all()
    return syncs


# CRM router
app.include_router(crm_router)
