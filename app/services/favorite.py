from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.models.favorite import Favorite
from app.core.models.place import Place
from app.core.exceptions import PlaceNotFound, FavoriteAlreadyExists, FavoriteNotFound

class FavoriteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_place_favorited(self, user_id: int, place_id: int) -> bool:
        stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.place_id == place_id)
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None

    async def add_favorite(self, user_id: int, place_id: int) -> Favorite:
        place = await self.db.get(Place, place_id)
        if not place:
            raise PlaceNotFound(f"Місце з ID {place_id} не знайдено.")
        if await self.is_place_favorited(user_id, place_id):
            raise FavoriteAlreadyExists("Це місце вже є у ваших улюблених.")
        new_fav = Favorite(user_id=user_id, place_id=place_id)
        self.db.add(new_fav)
        await self.db.commit()
        await self.db.refresh(new_fav)
        return new_fav

    async def remove_favorite(self, user_id: int, place_id: int) -> None:
        stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.place_id == place_id)
        result = await self.db.execute(stmt)
        fav = result.scalars().first()
        if not fav:
            raise FavoriteNotFound("Це місце не було знайдено у ваших улюблених.")
        await self.db.delete(fav)
        await self.db.commit()

    async def get_user_favorites(self, user_id: int) -> List[Place]:
        stmt = select(Place).join(Favorite).where(Favorite.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
