import pytest
from httpx import AsyncClient

from tests.factories.user import UserFactory


@pytest.fixture()
def registration_payload(faker):
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "password": "StrongPassword123",
    }


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, registration_payload: dict):
    response = await client.post("/auth/register", json=registration_payload)

    assert response.status_code == 201
    data = response.json()

    assert data["email"] == registration_payload["email"]
    assert "token" in data


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient, user_factory: UserFactory,
                                             registration_payload: dict):
    existing_user = await user_factory()
    registration_payload["email"] = existing_user.email

    response = await client.post("/auth/register", json=registration_payload)

    assert response.status_code == 409
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient, user_factory: UserFactory):
    user = await user_factory(password_hash="$2b$12$R.S.W3.uGgZ8.Q3Z/x.c.eN.M5f4O2P4tLgD.J2.gY.k.rD7p.G4")

    login_payload = {
        "username": user.email,
        "password": "StrongPassword123",
    }

    response = await client.post("/auth/login", data=login_payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient, user_factory: UserFactory):
    await user_factory()

    invalid_payload = {
        "username": "nonexistent@test.com",
        "password": "wrongpassword",
    }

    response = await client.post("/auth/login", data=invalid_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"