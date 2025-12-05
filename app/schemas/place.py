from pydantic import BaseModel, Field, conint
from typing import Optional


# Базова схема для створення та оновлення
class PlaceBaseSchema(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    # НОВЕ ПОЛЕ: Адреса
    address: Optional[str] = Field(None, max_length=255, description="Фізична адреса місця")

    latitude: float = Field(..., description="Широта місця")
    longitude: float = Field(..., description="Довгота місця")
    image_url: Optional[str] = Field(None, description="URL зображення")

    # Додаткові поля, які тепер можна задавати при створенні
    is_new: Optional[bool] = Field(True, description="Позначка, чи є місце новим")
    is_popular: Optional[bool] = Field(False, description="Позначка, чи є місце популярним")

    # ID категорії, до якої належить місце
    category_id: conint(ge=1) = Field(..., description="ID категорії")


# Схема для створення (успадковує базові поля)
class PlaceCreateSchema(PlaceBaseSchema):
    pass


# Схема для оновлення (всі поля необов'язкові)
class PlaceUpdateSchema(BaseModel):  # ВИПРАВЛЕНО: Успадкування від BaseModel
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = Field(None, max_length=255)
    latitude: Optional[float] = Field(None)
    longitude: Optional[float] = Field(None)
    image_url: Optional[str] = Field(None)
    is_new: Optional[bool] = Field(None)
    is_popular: Optional[bool] = Field(None)
    category_id: Optional[conint(ge=1)] = Field(None)


# Схема для відповіді API
class PlaceResponseSchema(BaseModel):  # ВИПРАВЛЕНО: Успадкування від BaseModel
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

    # Додаємо конфігурацію SQLAlchemy
    class Config:
        from_attributes = True


# Схема для вбудовування Category у Place (щоб у відповіді бачити ім'я категорії)
class CategorySimpleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Розширена схема відповіді, що включає Category
class PlaceDetailedResponseSchema(PlaceResponseSchema):
    category: CategorySimpleSchema