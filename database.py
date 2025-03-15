from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base  # Импортируем Base из models.py

# Настройка подключения к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"  # Замените на свои данные

# Асинхронный движок для PostgreSQL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция для получения асинхронной сессии
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# Создание таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)