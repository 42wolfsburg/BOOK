# .env          → stores the raw values (passwords, credentials)
# config.py     → reads .env and makes them available in Python
# database.py   → imports config.py to get database credentials
# Stop using AI to generate your stuff

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	POSTGRES_HOST: str
	POSTGRES_PORT: int
	BACKEND_HOST: str
	BACKEND_PORT: int
	DATABASE_URL: str
	VITE_API_URL: str
	VITE_42_SECRET: str
	VITE_42_CLIENT_ID: str
	VITE_42_REDIRECT_URI: str
	model_config = ConfigDict(env_file=".env")

settings = Settings()