from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
<<<<<<< HEAD
from models import Base

# Настройка подключения к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:botya1102@localhost:5432/postgres"
#SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://mental_user:9xErr3ms7R0m0P1F@46.37.123.171:5432/mental_db"

# Создаем асинхронный движок
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем фабрику сессий
=======
from models import Base  # Импортируем Base из models.py

# Настройка подключения к PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:botya1102@localhost:5432/postgres"

# Асинхронный движок для PostgreSQL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Асинхронная сессия
>>>>>>> 3d0d311636e66caa5d8b7bcfe061b93cf59098c4
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

<<<<<<< HEAD
# Функция для получения сессии (Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Функция создания таблиц
=======
# Функция для получения асинхронной сессии
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# Создание таблиц в базе данных
>>>>>>> 3d0d311636e66caa5d8b7bcfe061b93cf59098c4
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)