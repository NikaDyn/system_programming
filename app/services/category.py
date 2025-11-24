from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.models.category import Category
from app.schemas.category import CategoryCreateSchema, CategoryUpdateSchema
from app.core.exceptions import CategoryNotFound, CategoryAlreadyExists

class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        result = await self.db.execut
