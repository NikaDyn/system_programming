from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import Database as db
from app.core.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategoryResponseSchema, CategoryUpdateSchema


router = APIRouter(prefix="/categories", tags=["Categories"])


async def get_session() -> AsyncSession:
    async with db.session_maker() as session:
        yield session


@router.post("/", response_model=CategoryResponseSchema)
async def create_category(data: CategoryCreateSchema, session: AsyncSession = Depends(get_session)):
    category = Category(**data.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


@router.get("/", response_model=list[CategoryResponseSchema])
async def get_categories(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Category))
    return result.scalars().all()


@router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_category(category_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
