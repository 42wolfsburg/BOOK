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
	JWT_SECRET: str
	REDIRECT_URI: str
	CLIENT_ID: str
	SECRET: str
	FRONTEND_URL: str
	VITE_API_URL: str
	GOOGLE_CREDENTIALS_PISCINE_B64: str
	GOOGLE_CREDENTIALS_GALAXY_B64: str
	GOOGLE_CREDENTIALS_SPACE_INVADER_B64: str
	GOOGLE_CREDENTIALS_GALLERY_B64: str

	model_config = ConfigDict(env_file=".env")

settings = Settings()