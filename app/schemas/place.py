from pydantic import BaseModel, Field
from typing import Optional


class PlaceCreateSchema(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    location: str = Field(max_length=200)
    category_id: int


class PlaceResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    location: str
    category_id: int

    class Config:
        orm_mode = True


class PlaceUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    location: Optional[str] = Field(default=None, max_length=200)
    category_id: Optional[int] = None
