from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.schemas.user import UserCreateSchema, UserResponseSchema, Token
from app.services.user import UserService
from app.dependencies import get_user_service, get_current_active_user
from app.core.exceptions import UserAlreadyExists
from app.core.security import create_access_token
from app.core.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserCreateSchema,
        user_service: UserService = Depends(get_user_service)
):
    try:
        new_user = await user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        return new_user
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач із такою електронною поштою вже існує."
        )

@router.post("/login", response_model=Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний email або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неактивний користувач"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponseSchema)
async def read_current_user(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
