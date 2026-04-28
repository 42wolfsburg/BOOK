# .env          → stores the raw values (passwords, credentials)
# config.py     → reads .env and makes them available in Python
# database.py   → imports config.py to get database credentials

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()