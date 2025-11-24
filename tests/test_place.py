import pytest


@pytest.mark.asyncio
async def test_create_place_success(client, category_factory):
    category = await category_factory.create_async()

    payload = {
        "name": "Best Restaurant",
        "description": "Tasty food",
        "category_id": category.id,
        "is_new": True,
        "is_popular": False
    }

    response = await client.post("/places/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["category_id"] == category.id


@pytest.mark.asyncio
async def test_get_places_list(client, place_factory):
    await place_factory.create_batch_async(3)

    response = await client.get("/places/")

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_filter_places_by_category(client, place_factory, category_factory):
    category1 = await category_factory.create_async()
    category2 = await category_factory.create_async()

    await place_factory.create_async(category=category1)
    await place_factory.create_async(category=category1)
    await place_factory.create_async(category=category2)

    response = await client.get(f"/places/?category_id={category1.id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for place in data:
        assert place["category_id"] == category1.id


@pytest.mark.asyncio
async def test_delete_place(client, place_factory):
    place = await place_factory.create_async()

    response = await client.delete(f"/places/{place.id}")
    assert response.status_code == 204

    response_get = await client.get(f"/places/{place.id}")
    assert response_get.status_code == 404