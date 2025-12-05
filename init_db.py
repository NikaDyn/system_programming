import asyncio
import os
import sys
from app.db import engine, db  # db - це DeclarativeBase
from app.core.models.user import User
# !!! ВАЖЛИВО: Імпортуйте ВСІ моделі тут, щоб їх метадані були відомі Base
from app.core.models import category, place, favorite  # Додайте всі ваші файли моделей

# Додаємо кореневий каталог проєкту до шляху пошуку, щоб імпорт 'app' працював
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


async def init_db():
    print("--- Ініціалізація бази даних та створення таблиць ---")

    # Асинхронно видаляємо всі старі таблиці (DROP)
    async with engine.begin() as conn:
        # Скидання бази даних, якщо вона існувала
        # await conn.run_sync(db.metadata.drop_all)

        # Створення всіх таблиць
        await conn.run_sync(db.metadata.create_all)

    print("Таблиці успішно створені.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())