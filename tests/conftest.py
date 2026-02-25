import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db import get_db, db
from app.core.security import get_current_user, get_current_admin_user
from app.core.models.user import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_db.sqlite3"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


MOCK_ADMIN_USER = User(id=1, email="admin@test.com", hashed_password="hashed", is_superuser=True)
MOCK_REGULAR_USER = User(id=2, email="user@test.com", hashed_password="hashed", is_superuser=False)


async def override_get_current_user_admin():
    return MOCK_ADMIN_USER


async def override_get_current_admin_user():
    return MOCK_ADMIN_USER


@pytest.fixture(scope="function")
async def admin_client(client: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_current_admin_user, None)