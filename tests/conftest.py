import pytest
import pytest_asyncio
from typing import AsyncGenerator, Any
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.models.base import BaseModel
from app.main import app as global_app
from app.db import get_db
from app.core.security import get_current_admin_user, get_current_user
from tests.factories.category import CategoryFactory
from tests.factories.place import PlaceFactory
from tests.factories.user import UserFactory

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine):
    async_session = async_sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(autouse=True)
async def clear_db(db_session: AsyncSession):
    for table in reversed(BaseModel.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()


@pytest.fixture
async def category_factory(db_session):
    CategoryFactory._meta.sqlalchemy_session = db_session
    return CategoryFactory


@pytest.fixture
async def place_factory(db_session):
    PlaceFactory._meta.sqlalchemy_session = db_session
    return PlaceFactory


@pytest.fixture
async def user_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    return UserFactory


@pytest.fixture
def app():
    return global_app


class MockUser:
    id = 1
    email = "admin@test.com"
    is_superuser = True
    is_active = True


@pytest_asyncio.fixture()
async def client(db_session) -> AsyncGenerator[AsyncClient, Any]:
    async def override_get_db():
        async with db_session as session:
            yield session

    global_app.dependency_overrides[get_db] = override_get_db
    global_app.dependency_overrides[get_current_admin_user] = lambda: MockUser()
    global_app.dependency_overrides[get_current_user] = lambda: MockUser()

    async with LifespanManager(global_app):
        transport = ASGITransport(app=global_app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

    global_app.dependency_overrides.clear()
