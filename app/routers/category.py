from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.schemas.category import CategoryCreateSchema, CategoryResponseSchema
from app.core.models.category import Category
from app.core.security import get_current_admin_user

router = APIRouter()


@router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_data: CategoryCreateSchema,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_admin_user)
):
    query = select(Category).where(Category.name == category_data.name)
    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category_data.name, description=category_data.description)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


@router.get("/", response_model=list[CategoryResponseSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    query = select(Category)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_category(
        category_id: int,
        db: AsyncSession = Depends(get_db)
):
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_admin_user)
):
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
    return None