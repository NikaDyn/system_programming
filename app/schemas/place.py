from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlaceBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_new: bool = False
    is_popular: bool = False
    category_id: int

class PlaceCreateSchema(PlaceBaseSchema):
    pass

class PlaceResponseSchema(PlaceBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)