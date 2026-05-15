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
	model_config = ConfigDict(env_file=".env")

    # class Config:
    #     env_file = ".env" # this class has been deprecated https://stackoverflow.com/questions/78031241/pydantic-userwarning-valid-config-keys-have-changed-in-v2

settings = Settings()