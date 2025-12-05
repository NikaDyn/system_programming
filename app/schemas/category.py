from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class CategoryCreateSchema(CategoryBase):
    pass


class CategoryUpdateSchema(CategoryBase):
    name: Optional[str] = None


class CategoryResponseSchema(CategoryBase):
    id: int = Field(...)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Ресторани",
            }
        }