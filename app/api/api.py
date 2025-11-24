from fastapi import APIRouter

# Імпортуємо всі роутери версії v1
from app.api.v1 import auth as auth_router
from app.api.v1 import category as category_router
from app.api.v1 import place as place_router

# Головний роутер для версії v1
api_v1_router = APIRouter(prefix="/v1")

# Включаємо роути в головний роутер v1
api_v1_router.include_router(auth_router.router)
api_v1_router.include_router(category_router.router)
api_v1_router.include_router(place_router.router)

# Головний роутер застосунку
api_router = APIRouter()

# Додаємо версію v1 до основного застосунку
api_router.include_router(api_v1_router)