from pydantic import BaseModel, Field


class FavoriteCreateSchema(BaseModel):
    user_id: int
    place_id: int


class FavoriteResponseSchema(BaseModel):
    id: int
    user_id: int
    place_id: int

    class Config:
        orm_mode = True
