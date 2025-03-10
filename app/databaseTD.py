from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# строка подключения к бд
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///todo.db"
# Создание асинхронного движка (соединение с бд)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создание асинхронного сеанса
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Зависимость для сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:  # Автоматическое закрытие сессии
        yield session
