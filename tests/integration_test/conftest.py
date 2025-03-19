import pytest

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.databaseTD import get_db
from app.models import Base
from app.main import app
from config import settings

from httpx import ASGITransport, AsyncClient

import asyncio
from typing import Any, Generator

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    #loop = asyncio.get_event_loop()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop
    loop.close()

@pytest.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        settings.TEST_DATABASE_URL,
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

    async with AsyncClient(
            transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()