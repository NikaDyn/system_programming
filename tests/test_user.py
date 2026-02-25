import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from tests.factories.user import UserFactory

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

VALID_PASSWORD = "StrongPassword123"
TEST_HASH = pwd_context.hash(VALID_PASSWORD)

PREFIX = "/users"


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "email": "newuser@example.com",
        "full_name": "Іван Іванов",
        "password": "securepassword"
    }
    response = await client.post(f"{PREFIX}/register", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient, db_session: AsyncSession):
    await UserFactory.create_async(session=db_session, email="existing@example.com")

    payload = {
        "email": "existing@example.com",
        "full_name": "Інше",
        "password": "securepassword"
    }
    response = await client.post(f"{PREFIX}/register", json=payload)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient, db_session: AsyncSession):
    await UserFactory.create_async(
        session=db_session,
        email="login@example.com",
        hashed_password=TEST_HASH
    )

    response = await client.post(f"{PREFIX}/login", data={"username": "login@example.com", "password": VALID_PASSWORD})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient, db_session: AsyncSession):
    await UserFactory.create_async(
        session=db_session,
        email="login2@example.com",
        hashed_password=TEST_HASH
    )

    response = await client.post(f"{PREFIX}/login",
                                 data={"username": "login2@example.com", "password": "wrongpassword"})
    assert response.status_code == 401