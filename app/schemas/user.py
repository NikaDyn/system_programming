from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseSchema(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreateSchema(UserBaseSchema):
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
