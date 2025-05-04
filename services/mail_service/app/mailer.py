import httpx
from .config import get_settings

async def send_email(to: str, subject: str, html: str) -> None:
    settings = get_settings()
    payload = {
        "from": settings.mail_from,
        "to":   [to],
        "subject": subject,
        "html": html,
    }
    headers = {"Authorization": f"Bearer {settings.resend_api_key}"}
    async with httpx.AsyncClient(base_url="https://api.resend.com") as client:
        r = await client.post("/emails", json=payload, headers=headers, timeout=10)
        r.raise_for_status()
