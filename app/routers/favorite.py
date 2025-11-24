from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db import get_db
from app.schemas.favorite import FavoriteCreateSchema, FavoriteResponseSchema
from app.core.models.favorite import Favorite
from app.core.models.place import Place
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=FavoriteResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
        fav_data: FavoriteCreateSchema,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    place = await db.get(Place, fav_data.place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    query = select(Favorite).where(
        Favorite.user_id == current_user.id,
        Favorite.place_id == fav_data.place_id
    )
    existing = await db.execute(query)
    if existing.scalar():
        raise HTTPException(status_code=400, detail="Already in favorites")

    new_fav = Favorite(user_id=current_user.id, place_id=fav_data.place_id)
    db.add(new_fav)
    await db.commit()

    query_reload = select(Favorite).where(Favorite.id == new_fav.id).options(selectinload(Favorite.place))
    result = await db.execute(query_reload)
    return result.scalar_one()


@router.get("/", response_model=list[FavoriteResponseSchema])
async def get_favorites(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    query = select(Favorite).where(Favorite.user_id == current_user.id).options(selectinload(Favorite.place))
    result = await db.execute(query)
    return result.scalars().all()


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_favorites(
        place_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    query = select(Favorite).where(
        Favorite.user_id == current_user.id,
        Favorite.place_id == place_id
    )
    result = await db.execute(query)
    fav = result.scalar_one_or_none()

    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")

    await db.delete(fav)
    await db.commit()
    return None