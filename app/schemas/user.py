from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreateSchema(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6)
