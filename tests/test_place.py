import pytest
from httpx import AsyncClient
from app.main import app
from tests.factories.place import PlaceFactory
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
async def test_filter_places_by_category(db_session):
    # Створюємо конкретну категорію
    cat = await CategoryFactory.create_async(name="Парки")
    # Створюємо місце в цій категорії
    await PlaceFactory.create_async(name="Центральний парк", category=cat)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Припускаємо, що у вас є фільтрація за category_id або просто перевіряємо список
        response = await ac.get("/places/")

    assert response.status_code == 200
    names = [place["name"] for place in response.json()]
    assert "Центральний парк" in names