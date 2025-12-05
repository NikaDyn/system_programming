import asyncio
import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from app.main import app
from app.db import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.core.models.user import User


class MockAsyncSession:
    def __init__(self):
        self.mock_results = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def add(self, *args, **kwargs): pass

    async def commit(self): pass

    async def refresh(self, *args, **kwargs): pass

    async def execute(self, *args, **kwargs): return self

    def scalar_one(self): return None

    def scalars(self): return self

    def all(self): return self.mock_results

    def first(self): return None

    def delete(self, *args, **kwargs): pass


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def override_get_db_dependency():
    app.dependency_overrides[get_db] = lambda: MockAsyncSession()
    yield
    app.dependency_overrides.clear()


MOCK_ADMIN_USER = User(id=1, email="admin@test.com", hashed_password="hashed", is_superuser=True)
MOCK_REGULAR_USER = User(id=2, email="user@test.com", hashed_password="hashed", is_superuser=False)


async def override_get_current_user_admin():
    return MOCK_ADMIN_USER


async def override_get_current_user_regular():
    return MOCK_REGULAR_USER


async def override_get_current_admin_user():
    return MOCK_ADMIN_USER


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def admin_client(client) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_current_user] = override_get_current_user_admin
    app.dependency_overrides[get_current_admin_user] = override_get_current_admin_user
    yield client
    del app.dependency_overrides[get_current_user]
    del app.dependency_overrides[get_current_admin_user]


@pytest.fixture
async def authorized_client(client) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_current_user] = override_get_current_user_regular
    yield client
    del app.dependency_overrides[get_current_user]