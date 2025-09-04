from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "ExpenseTracker"
    ENV: str = "dev"
    
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    POSTGRES_USER:str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | List[str] | str="*"
    
    CURRENCY_API_BASE: str | None = None
    BASE_CURRENCY: str = "INR"
    
    class Config:
        env_file = ".env"
        
settings = Settings()

