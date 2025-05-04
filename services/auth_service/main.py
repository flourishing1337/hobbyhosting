from auth_service.routes.auth import router as auth_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router)
