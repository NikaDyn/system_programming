import pytest
from httpx import AsyncClient

from tests.factories.place import PlaceFactory, CategoryFactory


@pytest.fixture()
def place_payload(faker):
    return {
        "name": faker.company_name(),
        "description": faker.paragraph(nb_sentences=3),
        "address": faker.street_address(),
        "theme": faker.word(),
        "is_new": faker.boolean(),
        "is_popular": faker.boolean(),
        "latitude": faker.latitude(),
        "longitude": faker.longitude(),
    }


@pytest.mark.asyncio
async def test_create_place_success(client: AsyncClient, place_payload: dict, category_factory: CategoryFactory):
    category = await category_factory()
    payload_with_category = {**place_payload, "category_id": category.id}

    headers = {"Authorization": "Bearer admin_token_for_test"}

    response = await client.post("/places/", json=payload_with_category, headers=headers)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == payload_with_category["name"]
    assert data["category_id"] == category.id
    assert "id" in data


@pytest.mark.asyncio
async def test_get_place_by_id(client: AsyncClient, place_factory: PlaceFactory):
    place = await place_factory()

    response = await client.get(f"/places/{place.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == place.id
    assert data["name"] == place.name
    assert data["theme"] == place.theme


@pytest.mark.asyncio
async def test_get_nonexistent_place(client: AsyncClient):
    response = await client.get("/places/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Place not found"


@pytest.mark.asyncio
async def test_get_all_places_unfiltered(client: AsyncClient, place_factory: PlaceFactory):
    [await place_factory() for _ in range(3)]

    response = await client.get("/places/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_filter_places_by_category(client: AsyncClient, place_factory: PlaceFactory,
                                         category_factory: CategoryFactory):
    food_category = await category_factory(name='Food')
    walk_category = await category_factory(name='Walking')

    await place_factory(category=food_category)
    await place_factory(category=food_category)
    await place_factory(category=walk_category)

    response = await client.get("/places/?category_name=Food")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert all(d['category_id'] == food_category.id for d in data)


@pytest.mark.asyncio
async def test_filter_places_by_is_new_and_is_popular(client: AsyncClient, place_factory: PlaceFactory):
    await place_factory(is_new=True, is_popular=True)
    await place_factory(is_new=False, is_popular=True)
    await place_factory(is_new=True, is_popular=False)
    await place_factory(is_new=False, is_popular=False)

    response_new = await client.get("/places/?is_new=true")
    assert response_new.status_code == 200
    assert len(response_new.json()) == 2

    response_popular = await client.get("/places/?is_popular=true")
    assert response_popular.status_code == 200
    assert len(response_popular.json()) == 2

    response_both = await client.get("/places/?is_new=true&is_popular=true")
    assert response_both.status_code == 200
    assert len(response_both.json()) == 1


@pytest.mark.asyncio
async def test_admin_update_place_data(client: AsyncClient, place_factory: PlaceFactory, faker):
    place = await place_factory(name="Old Name")
    new_description = faker.paragraph(nb_sentences=2)

    partial_payload = {
        "description": new_description,
        "is_new": True
    }

    headers = {"Authorization": "Bearer admin_token_for_test"}
    response = await client.patch(f"/places/{place.id}", json=partial_payload, headers=headers)

    assert response.status_code == 200
    data = response.json()

    assert data["description"] == new_description
    assert data["is_new"] == True
    assert data["name"] == "Old Name"


@pytest.mark.asyncio
async def test_admin_delete_place(client: AsyncClient, place_factory: PlaceFactory):
    place_to_delete = await place_factory()

    headers = {"Authorization": "Bearer admin_token_for_test"}
    response = await client.delete(f"/places/{place_to_delete.id}", headers=headers)

    assert response.status_code == 204

    check_response = await client.get(f"/places/{place_to_delete.id}")
    assert check_response.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_admin_action(client: AsyncClient, place_factory: PlaceFactory, place_payload: dict):
    response_create = await client.post("/places/", json=place_payload)

    assert response_create.status_code in (401, 403)

    place = await place_factory()
    response_delete = await client.delete(f"/places/{place.id}")

    assert response_delete.status_code in (401, 403)