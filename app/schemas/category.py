from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryResponseSchema(CategoryBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)