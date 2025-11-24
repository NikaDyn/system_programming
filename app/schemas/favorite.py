from pydantic import BaseModel, ConfigDict
from app.schemas.place import PlaceResponseSchema

class FavoriteCreateSchema(BaseModel):
    place_id: int

class FavoriteResponseSchema(BaseModel):
    id: int
    user_id: int
    place_id: int
    # Ми хочемо бачити деталі місця, коли дивимось список улюбленого
    place: PlaceResponseSchema

    model_config = ConfigDict(from_attributes=True)