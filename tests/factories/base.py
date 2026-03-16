import factory
from factory.alchemy import SQLAlchemyModelFactory

class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'

    @classmethod
    async def create_async(cls, **kwargs):
        """Асинхронне створення одного об'єкта для тестів."""
        instance = cls.build(**kwargs)
        session = cls._meta.sqlalchemy_session
        if not session:
            raise RuntimeError("SQLAlchemy session is not set for the factory. Check your conftest.py")

        session.add(instance)
        await session.flush()  # Використовуємо flush замість commit, щоб тест керував транзакцією
        return instance

    @classmethod
    async def create_batch_async(cls, size, **kwargs):
        """Асинхронне створення списку об'єктів."""
        return [await cls.create_async(**kwargs) for _ in range(size)]