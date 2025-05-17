import logging
from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .dependencies import engine, get_db
from .hashing import hash_password, verify_password
from .jwt_utils import create_token, get_current_admin, security, verify_token
from .models import Base, User
from .schemas import TokenOut, UserCreate, UserOut

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Init DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hobbyhosting.org",
        "https://admin.hobbyhosting.org",
        "https://ecom.hobbyhosting.org",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/auth/health")
def health():
    return {"status": "ok"}


@app.post("/auth/login", response_model=TokenOut)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        content_type = request.headers.get("content-type", "")
        if content_type.startswith("application/json"):
            data = await request.json()
            username = data.get("username")
            password = data.get("password")
        else:
            form = await request.form()
            username = form.get("username")
            password = form.get("password")

        logger.info(f"Login attempt for user: {username}")

        if not username or not password:
            logger.warning("Missing username or password")
            raise HTTPException(
                status_code=400, detail="Username and password are required"
            )

        user = db.query(User).filter(User.username == username).first()
        logger.debug(f"User lookup result: {user is not None}")

        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid login attempt for user: {username}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        logger.info(f"Successful login for user: {username}")
        return {"access_token": create_token(user.username, user.is_admin)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/auth/refresh", response_model=TokenOut)
async def refresh(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, detail="Invalid token format")

    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    username = payload["sub"]

    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(401, detail="User not found")

    return {"access_token": create_token(user.username, user.is_admin)}


@app.get("/auth/me", response_model=UserOut)
def read_me(auth: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(auth.credentials)
    username = payload["sub"]
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    return UserOut.model_validate(user)


@app.post("/auth/register", status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(400, detail="Username already exists")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        is_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "message": "User created"}


@app.get("/users", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db), current=Depends(get_current_admin)):
    return db.query(User).all()


@app.post("/auth/promote")
def promote_user(
    username: str = Body(...),
    db: Session = Depends(get_db),
    current=Depends(get_current_admin),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    user.is_admin = True
    db.commit()
    return {"message": f"{username} is now admin"}


@app.post("/auth/demote")
def demote_user(
    username: str = Body(...),
    db: Session = Depends(get_db),
    current=Depends(get_current_admin),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(404, detail="User not found")
    user.is_admin = False
    db.commit()
    return {"message": f"{username} is no longer admin"}
