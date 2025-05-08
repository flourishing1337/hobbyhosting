import json

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .dependencies import engine, get_db
from .hashing import hash_password, verify_password
from .jwt_utils import create_token
from .models import Base, User
from .schemas import TokenOut, UserCreate

# ------------- init -------------
Base.metadata.create_all(bind=engine)  # auto-skapa tabeller om de saknas

app = FastAPI(title="Auth Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hobbyhosting.org",
        "https://admin.hobbyhosting.org",
        "https://ecom.hobbyhosting.org",
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- endpoints -----------


@app.get("/auth/health")
def health():
    return {"status": "ok"}


@app.post("/auth/login", response_model=TokenOut)
async def login(request: Request):
    try:
        # Get raw body and log it
        body = await request.body()
        body_str = body.decode()
        print(f"Received login request with body: {body_str}")

        # Parse body manually
        data = json.loads(body_str)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required",
            )

        # Get DB session
        db = next(get_db())

        # Find user and verify password
        user: User | None = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return {"access_token": create_token(user.username)}
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format"
        )
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    # Debug logging
    body = await request.body()
    print(f"Received registration request with body: {body.decode()}")

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        is_admin=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "message": "Admin user created 🎉"}
