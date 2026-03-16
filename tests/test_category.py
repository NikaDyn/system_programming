import pytest
from httpx import AsyncClient
from app.main import app
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
async def test_get_all_categories_api(db_session):
    # Створюємо 3 випадкові категорії
    await CategoryFactory.create_batch_async(3)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/categories/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3