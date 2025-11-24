from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_
from app.core.models.place import Place
from app.core.models.category import Category
from app.schemas.place import PlaceCreateSchema, PlaceUpdateSchema
from app.core.exceptions import PlaceNotFound, CategoryNotFound, PermissionDenied

class PlaceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_place_by_id(self, place_id: int) -> Optional[Place]:
        result = await self.db.execute(select(Place).where(Place.id == place_id))
        return result.scalars().first()

    async def create_place(self, place_in: PlaceCreateSchema, owner_id: int) -> Place:
        category = await self.db.get(Category, place_in.category_id)
        if not category:
            raise CategoryNotFound(f"Категорію з ID {place_in.category_id} не знайдено.")
        new_place = Place(
            name=place_in.name,
            description=place_in.description,
            address=place_in.address,
            latitude=place_in.latitude,
            longitude=place_in.longitude,
            category_id=place_in.category_id,
            owner_id=owner_id,
            rating=0.0
        )
        self.db.add(new_place)
        await self.db.commit()
        await self.db.refresh(new_place)
        return new_place

    async def update_place(self, place_id: int, place_in: PlaceUpdateSchema, current_user_id: int, is_superuser: bool) -> Place:
        db_place = await self.get_place_by_id(place_id)
        if not db_place:
            raise PlaceNotFound(f"Місце з ID {place_id} не знайдено.")
        if db_place.owner_id != current_user_id and not is_superuser:
            raise PermissionDenied("Недостатньо прав", "Ви можете оновлювати лише власні місця.")
        if place_in.category_id is not None and place_in.category_id != db_place.category_id:
            category = await self.db.get(Category, place_in.category_id)
            if not category:
                raise CategoryNotFound(f"Категорію з ID {place_in.category_id} не знайдено.")
        for field, value in place_in.model_dump(exclude_unset=True).items():
            setattr(db_place, field, value)
        self.db.add(db_place)
        await self.db.commit()
        await self.db.refresh(db_place)
