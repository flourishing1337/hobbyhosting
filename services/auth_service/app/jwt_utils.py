from datetime import datetime, timedelta
import jwt
from .config import get_settings

settings = get_settings()

def create_token(sub: str, expires: int = 60 * 24) -> str:        # 24 h default
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "iat": now,
        "exp": now + timedelta(minutes=expires),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
