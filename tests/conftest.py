import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.database import Base
from tests.factories.user import UserFactory
from tests.factories.place import PlaceFactory
from tests.factories.category import CategoryFactory
from tests.factories.favorite import FavoriteFactory

# Використовуємо SQLite в пам'яті для швидкості тестів
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Створює чисту базу даних для кожного тесту."""
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with Session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def setup_factories(db_session):
    """Автоматично прив'язує поточну сесію до всіх фабрик перед тестом."""
    factories = [UserFactory, PlaceFactory, CategoryFactory, FavoriteFactory]
    for f in factories:
        f._meta.sqlalchemy_session = db_session
    yield
    for f in factories:
        f._meta.sqlalchemy_session = None