import asyncio
import os
import sys
from dotenv import load_dotenv

# Додаємо кореневий каталог проєкту до шляху пошуку, щоб імпорт 'app' працював
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# !!! КРИТИЧНО: Використовуємо абсолютний імпорт для User,
# але імпортуємо інші моделі безпосередньо, щоб вони були зареєстровані
from app.db import get_db, engine
from app.core.models.user import User

# ГАРАНТУЄМО, що ВСІ моделі зареєстровані шляхом прямого імпорту:
import app.core.models.category
import app.core.models.place
import app.core.models.favorite
# --------------------------------------------------------------------------

from app.core.security import get_password_hash
from sqlalchemy import select

# --- Конфігурація Суперкористувача ---
SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL", "admin@explorer.com")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD", "strong_admin_password")
SUPERUSER_FULL_NAME = "System Administrator"


# ------------------------------------

async def create_superuser():
    """Створює суперкористувача, якщо він ще не існує."""
    print("--- Створення Суперкористувача ---")

    async for session in get_db():
        try:
            # 1. Перевірка, чи користувач вже існує
            query = select(User).where(User.email == SUPERUSER_EMAIL)
            result = await session.execute(query)
            admin_user = result.scalar_one_or_none()

            if admin_user:
                # 2. Якщо користувач існує, просто оновлюємо його
                admin_user.is_superuser = True
                admin_user.hashed_password = get_password_hash(SUPERUSER_PASSWORD)
                print(f"Користувач '{SUPERUSER_EMAIL}' вже існує. Оновлено до суперкористувача.")
            else:
                # 3. Якщо користувач не існує, створюємо його
                hashed_password = get_password_hash(SUPERUSER_PASSWORD)
                admin_user = User(
                    email=SUPERUSER_EMAIL,
                    full_name=SUPERUSER_FULL_NAME,
                    hashed_password=hashed_password,
                    is_superuser=True,
                    is_active=True
                )
                session.add(admin_user)
                print(f"Створено нового суперкористувача: {SUPERUSER_EMAIL}")

            await session.commit()

            await session.refresh(admin_user)
            print(f"ID адміністратора: {admin_user.id}")
            print(f"Статус суперкористувача: {admin_user.is_superuser}")
            print("Суперкористувач успішно створений/оновлений.")

        except Exception as e:
            await session.rollback()
            print(f"Помилка під час створення суперкористувача: {e}")

    await engine.dispose()


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(create_superuser())