import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.place import PlaceFactory
from tests.factories.category import CategoryFactory


@pytest.mark.asyncio
async def test_get_nonexistent_place(client: AsyncClient):
    response = await client.get("/places/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_place_success(admin_client: AsyncClient, db_session: AsyncSession):
    category = await CategoryFactory.create_async(session=db_session)

    place_data = {
        "name": "Тестове місце",
        "description": "Гарний опис",
        "address": "м. Київ",
        "latitude": 50.4501,
        "longitude": 30.5234,
        "is_new": True,
        "is_popular": False,
        "category_id": category.id
    }

    response = await admin_client.post("/places/", json=place_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_place_by_id(client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    place = await PlaceFactory.create_async(session=db_session, category_id=cat.id)

    response = await client.get(f"/places/{place.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_places_unfiltered(client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    await PlaceFactory.create_async(session=db_session, category_id=cat.id)
    await PlaceFactory.create_async(session=db_session, category_id=cat.id)

    response = await client.get("/places/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


@pytest.mark.asyncio
async def test_filter_places_by_category(client: AsyncClient, db_session: AsyncSession):
    cat1 = await CategoryFactory.create_async(session=db_session)
    cat2 = await CategoryFactory.create_async(session=db_session)

    await PlaceFactory.create_async(session=db_session, category_id=cat1.id)
    await PlaceFactory.create_async(session=db_session, category_id=cat2.id)

    response = await client.get(f"/places/?category_id={cat1.id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_filter_places_by_is_new_and_is_popular(client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    await PlaceFactory.create_async(session=db_session, category_id=cat.id, is_new=True, is_popular=False)
    await PlaceFactory.create_async(session=db_session, category_id=cat.id, is_new=False, is_popular=True)

    res_new = await client.get("/places/?is_new=true")
    assert res_new.status_code == 200
    res_pop = await client.get("/places/?is_popular=true")
    assert res_pop.status_code == 200


@pytest.mark.asyncio
async def test_admin_delete_place(admin_client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    place = await PlaceFactory.create_async(session=db_session, category_id=cat.id)
    response = await admin_client.delete(f"/places/{place.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_unauthorized_admin_action(client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    place = await PlaceFactory.create_async(session=db_session, category_id=cat.id)
    response = await client.delete(f"/places/{place.id}")
    assert response.status_code in [401, 403]