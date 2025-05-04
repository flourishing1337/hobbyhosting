# mail_service/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_202_ACCEPTED
from .schemas import MailRequest
from .mailer  import send_email
from .config  import get_settings
from .security import get_current_user

app = FastAPI(title="HobbyHosting Mail-service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/send", status_code=HTTP_202_ACCEPTED)
async def send(
    req: MailRequest,
    current_user = Depends(get_current_user)  # ⬅️ kräver JWT
):
    try:
        await send_email(req.to, req.subject, req.html)
        return {"status": "ok"}
    except Exception as exc:
        raise HTTPException(502, detail=str(exc))
