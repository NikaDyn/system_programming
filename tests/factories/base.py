import factory


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        # Важливо: вимикаємо стандартне збереження, бо воно синхронне
        sqlalchemy_session_persistence = None

    @classmethod
    async def create_async(cls, **kwargs):
        """Асинхронне створення одного об'єкта"""
        # 1. Створюємо об'єкт (синхронно)
        instance = cls.build(**kwargs)

        # 2. Отримуємо сесію
        session = cls._meta.sqlalchemy_session
        if not session:
            raise RuntimeError("Session not set in Factory")

        # 3. Зберігаємо в БД (асинхронно)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def create_batch_async(cls, size, **kwargs):
        """Асинхронне створення списку об'єктів"""
        return [await cls.create_async(**kwargs) for _ in range(size)]