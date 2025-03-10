import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.databaseTD import get_db
from app.models import Base
from app.main import app
from sqlalchemy.pool import StaticPool

from httpx import AsyncClient

# Создаем асинхронный движок для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///testing.db"
# TEST_DATABASE_URL = (
#     "sqlite+aiosqlite:///:memory:"  # Создает бд в памяти (без файла на жестком диске)
# )


@pytest.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = async_sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(name="client")
async def client_fixture(session: AsyncSession):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_db] = get_session_override
    """
    async with AsyncClient() as client:
        yield client
"""
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
