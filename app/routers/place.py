from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.schemas.place import PlaceCreateSchema, PlaceResponseSchema
from app.core.models.place import Place
from app.core.security import get_current_admin_user

router = APIRouter()


@router.post("/", response_model=PlaceResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_place(
        place_data: PlaceCreateSchema,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_admin_user)
):
    new_place = Place(
        name=place_data.name,
        description=place_data.description,
        address=place_data.address,
        latitude=place_data.latitude,
        longitude=place_data.longitude,
        is_new=place_data.is_new,
        is_popular=place_data.is_popular,
        category_id=place_data.category_id
    )
    db.add(new_place)
    await db.commit()
    await db.refresh(new_place)
    return new_place


@router.get("/", response_model=list[PlaceResponseSchema])
async def get_places(
        category_id: int | None = Query(None),
        is_new: bool | None = Query(None),
        is_popular: bool | None = Query(None),
        db: AsyncSession = Depends(get_db)
):
    query = select(Place)

    if category_id:
        query = query.where(Place.category_id == category_id)
    if is_new is not None:
        query = query.where(Place.is_new == is_new)
    if is_popular is not None:
        query = query.where(Place.is_popular == is_popular)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{place_id}", response_model=PlaceResponseSchema)
async def get_place_by_id(
        place_id: int,
        db: AsyncSession = Depends(get_db)
):
    place = await db.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place(
        place_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_admin_user)
):
    place = await db.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    await db.delete(place)
    await db.commit()
    return None