import pytest
from httpx import AsyncClient

from tests.factories.category import CategoryFactory


@pytest.fixture()
def category_payload(faker):
    return {
        "name": faker.word().capitalize() + " Category"
    }


@pytest.mark.asyncio
async def test_create_category_admin_success(client: AsyncClient, category_payload: dict):
    headers = {"Authorization": "Bearer admin_token"}
    response = await client.post("/categories/", json=category_payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_payload["name"]


@pytest.mark.asyncio
async def test_create_category_unauthorized(client: AsyncClient, category_payload: dict):
    response = await client.post("/categories/", json=category_payload)

    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_get_categories_list(client: AsyncClient, category_factory: CategoryFactory):
    await category_factory(name="Food")
    await category_factory(name="Walking")

    response = await client.get("/categories/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Food" in [c["name"] for c in data]


@pytest.mark.asyncio
async def test_delete_category_admin_success(client: AsyncClient, category_factory: CategoryFactory):
    category = await category_factory()
    headers = {"Authorization": "Bearer admin_token"}

    response = await client.delete(f"/categories/{category.id}", headers=headers)

    assert response.status_code == 204

    check_response = await client.get(f"/categories/{category.id}")
    assert check_response.status_code == 404