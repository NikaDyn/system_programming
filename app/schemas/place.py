from pydantic import BaseModel, Field, conint
from typing import Optional


class PlaceBaseSchema(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    address: Optional[str] = Field(None, max_length=255, description="Фізична адреса місця")

    latitude: float = Field(..., description="Широта місця")
    longitude: float = Field(..., description="Довгота місця")
    image_url: Optional[str] = Field(None, description="URL зображення")

    is_new: Optional[bool] = Field(True, description="Позначка, чи є місце новим")
    is_popular: Optional[bool] = Field(False, description="Позначка, чи є місце популярним")

    category_id: conint(ge=1) = Field(..., description="ID категорії")


class PlaceCreateSchema(PlaceBaseSchema):
    pass


class PlaceUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)
    image_url: Optional[str] = Field(None)
    is_new: Optional[bool] = Field(None)
    is_popular: Optional[bool] = Field(None)
    category_id: Optional[conint(ge=1)] = Field(None)


class PlaceResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float
    image_url: Optional[str]
    is_new: bool
    is_popular: bool
    category_id: int

    class Config:
        from_attributes = True


class CategorySimpleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PlaceDetailedResponseSchema(PlaceResponseSchema):
    category: CategorySimpleSchema