import pytest
from app.core.security import get_password_hash


@pytest.mark.asyncio
async def test_register_user_success(client):
    payload = {
        "email": "newuser@example.com",
        "password": "strongpassword123",
        "full_name": "New User"
    }

    response = await client.post("/users/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client, user_factory):
    existing_user = await user_factory.create_async(email="duplicate@test.com")

    payload = {
        "email": "duplicate@test.com",
        "password": "password123",
        "full_name": "Another User"
    }

    response = await client.post("/users/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_user_success(client, user_factory):
    password = "mypassword"
    hashed = get_password_hash(password)
    user = await user_factory.create_async(email="login@test.com", hashed_password=hashed)

    payload = {
        "email": "login@test.com",
        "password": password
    }

    response = await client.post("/users/login", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client, user_factory):
    await user_factory.create_async(email="wrong@test.com")

    payload = {
        "email": "wrong@test.com",
        "password": "wrongpassword"
    }

    response = await client.post("/users/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"