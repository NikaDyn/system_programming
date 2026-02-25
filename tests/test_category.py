import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.category import CategoryFactory

@pytest.mark.asyncio
async def test_create_category_admin_success(admin_client: AsyncClient):
    response = await admin_client.post("/categories/", json={"name": "Нова категорія"})
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_categories_list(client: AsyncClient, db_session: AsyncSession):
    await CategoryFactory.create_async(session=db_session, name="Категорія 1")
    await CategoryFactory.create_async(session=db_session, name="Категорія 2")

    response = await client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) >= 2