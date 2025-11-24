import pytest
from app.core.security import get_current_user
from app.main import app
from tests.factories.user import UserFactory


def override_user(user):
    return lambda: user


@pytest.mark.asyncio
async def test_add_to_favorites_success(client, app, place_factory, user_factory):
    user = await UserFactory.create_async()
    app.dependency_overrides[get_current_user] = override_user(user)

    place = await place_factory.create_async()

    response = await client.post("/favorites/", json={"place_id": place.id})

    assert response.status_code == 201
    data = response.json()
    assert data["place_id"] == place.id
    assert data["place"]["name"] == place.name


@pytest.mark.asyncio
async def test_get_favorites_list(client, app, place_factory, user_factory):
    user = await UserFactory.create_async()
    app.dependency_overrides[get_current_user] = override_user(user)

    place1 = await place_factory.create_async()
    place2 = await place_factory.create_async()

    await client.post("/favorites/", json={"place_id": place1.id})
    await client.post("/favorites/", json={"place_id": place2.id})

    response = await client.get("/favorites/")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_remove_from_favorites_success(client, app, place_factory, user_factory):
    user = await UserFactory.create_async()
    app.dependency_overrides[get_current_user] = override_user(user)

    place = await place_factory.create_async()
    await client.post("/favorites/", json={"place_id": place.id})

    response = await client.delete(f"/favorites/{place.id}")
    assert response.status_code == 204

    response_list = await client.get("/favorites/")
    assert len(response_list.json()) == 0