import pytest


@pytest.mark.asyncio
async def test_get_categories_empty(client):
    """Перевіряємо, що спочатку список порожній"""
    response = await client.get("/categories/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_categories_list(client, category_factory):
    """Створюємо 3 категорії через фабрику і перевіряємо, чи API їх бачить"""
    # ВИПРАВЛЕННЯ: використовуємо create_batch_async
    await category_factory.create_batch_async(3)

    response = await client.get("/categories/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "id" in data[0]
    assert "name" in data[0]


@pytest.mark.asyncio
async def test_create_category(client):
    """Перевірка створення категорії"""
    payload = {
        "name": "Coffee Shops",
        "description": "Best coffee in Frankivsk"
    }

    # Створення
    response = await client.post("/categories/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]

    # Перевірка дубліката (очікуємо 400)
    response_duplicate = await client.post("/categories/", json=payload)
    assert response_duplicate.status_code == 400


@pytest.mark.asyncio
async def test_get_single_category(client, category_factory):
    """Отримання однієї категорії по ID"""
    # ВИПРАВЛЕННЯ: використовуємо create_async
    category = await category_factory.create_async()

    response = await client.get(f"/categories/{category.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category.id
    assert data["name"] == category.name