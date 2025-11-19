from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import Database as db
from app.core.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreateSchema, FavoriteResponseSchema


router = APIRouter(prefix="/favorites", tags=["Favorites"])


async def get_session() -> AsyncSession:
    async with db.session_maker() as session:
        yield session


@router.post("/", response_model=FavoriteResponseSchema)
async def add_favorite(data: FavoriteCreateSchema, session: AsyncSession = Depends(get_session)):
    new_fav = Favorite(**data.model_dump())
    session.add(new_fav)
    await session.commit()
    await session.refresh(new_fav)
    return new_fav


@router.get("/", response_model=list[FavoriteResponseSchema])
async def get_favorites(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Favorite))
    return result.scalars().all()


@router.delete("/{favorite_id}", status_code=204)
async def delete_favorite(favorite_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Favorite).where(Favorite.id == favorite_id))
    favorite = result.scalar_one_or_none()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    await session.delete(favorite)
    await session.commit()
