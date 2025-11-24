from pydantic import BaseModel, EmailStr, ConfigDict

# Базова схема
class UserBaseSchema(BaseModel):
    email: EmailStr
    full_name: str | None = None

# Схема для реєстрації (вхідні дані)
class UserCreateSchema(UserBaseSchema):
    password: str

# Схема для логіну (вхідні дані)
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# Схема для відповіді (те, що бачить юзер після реєстрації)
class UserResponseSchema(UserBaseSchema):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Схема для токена
class TokenSchema(BaseModel):
    access_token: str
    token_type: str