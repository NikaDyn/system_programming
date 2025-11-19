from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import Database as db
from app.core.models.place import Place
from app.schemas.place import PlaceCreateSchema, PlaceResponseSchema, PlaceUpdateSchema


router = APIRouter(prefix="/places", tags=["Places"])


async def get_session() -> AsyncSession:
    async with db.session_maker() as session:
        yield session
