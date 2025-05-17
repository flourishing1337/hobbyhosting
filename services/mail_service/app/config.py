from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    resend_api_key: str
    mail_from: str = "noreply@hobbyhosting.org"
    # Secret and algorithm for verifying JWT tokens from auth_service
    jwt_secret: str
    jwt_algo: str = "HS256"

    class Config:
        env_file = ".env"  # laddas automatiskt av Pydantic


@lru_cache
def get_settings() -> Settings:
    return Settings()
