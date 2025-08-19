import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Settings:
    # Настройки базы данных (PostgreSQL)
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://mental_user:9xErr3ms7R0m0P1F@46.37.123.171:5432/mental_db")
    
    # Настройки JWT
    SECRET_KEY = os.getenv("your-secret-key", "your-secret-key-here-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Настройки Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
    
    # Другие настройки
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()