import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.main import app
from tests.factories.place import PlaceFactory
from tests.factories.category import CategoryFactory
from tests.factories.user import UserFactory


@pytest.fixture()
async def auth_client(client: AsyncClient, db_session: AsyncSession):
    user = await UserFactory.create_async(session=db_session)
    app.dependency_overrides[get_current_user] = lambda: user
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_add_to_favorites_success(auth_client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    place = await PlaceFactory.create_async(session=db_session, category_id=cat.id)

    response = await auth_client.post(f"/favorites/{place.id}")
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_favorites_list(auth_client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    place1 = await PlaceFactory.create_async(session=db_session, category_id=cat.id)
    place2 = await PlaceFactory.create_async(session=db_session, category_id=cat.id)

    await auth_client.post(f"/favorites/{place1.id}")
    await auth_client.post(f"/favorites/{place2.id}")

    response = await auth_client.get("/favorites/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_remove_from_favorites_success(auth_client: AsyncClient, db_session: AsyncSession):
    cat = await CategoryFactory.create_async(session=db_session)
    place = await PlaceFactory.create_async(session=db_session, category_id=cat.id)

    await auth_client.post(f"/favorites/{place.id}")
    response = await auth_client.delete(f"/favorites/{place.id}")
    assert response.status_code == 204