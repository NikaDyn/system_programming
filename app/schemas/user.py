from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=6)


class UserResponseSchema(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str