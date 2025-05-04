from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # ------- Runtime -------
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # ------- Databas -------
    DATABASE_URL: str

    # Pydantic kommer automatiskt läsa in från .env
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:       # singleton-cache
    return Settings()
