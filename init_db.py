import asyncio
import os
import sys
from app.db import engine, db  # db - це DeclarativeBase
from app.core.models.user import User

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


async def init_db():
    print("--- Ініціалізація бази даних та створення таблиць ---")

    async with engine.begin() as conn:
        await conn.run_sync(db.metadata.create_all)

    print("Таблиці успішно створені.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())