from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base

# Настройка подключения к PostgreSQL
<<<<<<< HEAD
#SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/postgres"
=======
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:343424343424@localhost:5433/postgres"
>>>>>>> f3bcd584c2dc08cd71ff003ee68ffd5ba8e383f4
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://mental_user:9xErr3ms7R0m0P1F@10.66.66.8:5432/mental_db"

# Создаем асинхронный движок
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция для получения сессии (Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Функция создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)