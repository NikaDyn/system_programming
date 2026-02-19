from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models.user import User
from app.core.security import get_current_user, get_current_admin_user
from app.core.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategoryResponseSchema
from app.db import get_db

router = APIRouter()

# === ВИПРАВЛЕНИЙ GET МЕТОД ===
@router.get("/", response_model=List[CategoryResponseSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    # Для асинхронної БД використовуємо select та await
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories

# === ВАШ ІСНУЮЧИЙ POST МЕТОД (залишається без змін) ===
@router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db),
    # Якщо ви використовуєте токен...
    current_user: User = Depends(get_current_admin_user)
):
    # ... ваш код створення категорії ...
    pass