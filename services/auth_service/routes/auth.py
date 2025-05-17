from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from shared.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

fake_users_db = {
    "admin@hobbyhosting.org": {
        "email": "admin@hobbyhosting.org",
        "password": "1337",
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login")
async def login(request: Request):
    try:
        # Debug logging
        print(f"Headers: {request.headers}")
        body = await request.body()
        print(f"Raw body: {body.decode()}")

        # Parse form data manually
        form_data = {}
        for item in body.decode().split("&"):
            key, value = item.split("=")
            from urllib.parse import unquote_plus

            form_data[key] = unquote_plus(value)

        print(f"Parsed form data: {form_data}")

        username = form_data.get("username")
        password = form_data.get("password")

        if not username or not password:
            return JSONResponse(status_code=400, detail="Missing username or password")

        user = fake_users_db.get(username)
        if not user or user["password"] != password:
            return JSONResponse(
                status_code=401, content={"detail": "Invalid credentials"}
            )

        access_token = create_access_token(data={"sub": username})
        return JSONResponse(
            status_code=200,
            content={"access_token": access_token, "token_type": "bearer"},
        )
    except Exception as e:
        import traceback

        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"detail": str(e)})


@router.get("/health")
async def health_check():
    return {"status": "ok"}
