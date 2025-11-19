from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str = Field(max_length=50)


class CategoryResponseSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
