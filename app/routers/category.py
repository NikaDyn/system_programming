from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.core.models.user import User
from app.core.security import get_current_user, get_current_admin_user
from app.core.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategoryResponseSchema

router = APIRouter()


@router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_data: CategoryCreateSchema,
        db: AsyncSession = Depends(get_db),
        # Якщо ви використовуєте токен адміністратора, залишайте get_current_admin_user
        current_user: User = Depends(get_current_admin_user)
):
    """Створення нової категорії. Дозволено лише для адміністраторів."""

    # 1. Перевіряємо, чи існує категорія з таким іменем (асинхронно)
    # Використовуємо db.scalar для отримання одного результату або None
    existing_category = await db.scalar(
        select(Category).where(Category.name == category_data.name)
    )

    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    # 2. Створюємо новий об'єкт моделі з Pydantic-даних
    new_category = Category(**category_data.model_dump())

    # 3. Зберігаємо в БД
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)  # Важливо для отримання ID

    return new_category