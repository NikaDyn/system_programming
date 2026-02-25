import factory
from factory.alchemy import SQLAlchemyModelFactory


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    async def create_async(cls, session, **kwargs):
        """
        Асинхронне створення об'єкта.
        session передається напряму, щоб уникнути втрати в SubFactory.
        """
        instance = cls.build(**kwargs)

        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def create_batch_async(cls, session, size, **kwargs):
        return [await cls.create_async(session=session, **kwargs) for _ in range(size)]