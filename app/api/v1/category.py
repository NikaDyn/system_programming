from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Annotated

from app.schemas.category import CategoryRead, CategoryCreate, CategoryUpdate
from app.services.category import CategoryService
from app.dependencies import get_category_service, get_current_superuser
from app.core.models.user import User # Для аннотації залежності суперкористувача

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    # Обмеження доступу: тільки суперкористувач може створювати категорії
    current_superuser: Annotated[User, Depends(get_current_superuser)]
):
    """
    Створити нову категорію. Доступно лише адміністраторам.
    """
    try:
        new_category = await category_service.create_category(category_data)
        return new_category
    except Exception as e:
        # Може виникнути помилка унікальності, якщо CategoryService її не обробляє
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[CategoryRead])
async def read_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    """
    Отримати список усіх категорій.
    """
    categories = await category_service.get_all_categories()
    return categories

@router.get("/{category_id}", response_model=CategoryRead)
async def read_category_by_id(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)]
):
    """
    Отримати категорію за її ID.
    """
    category = await category_service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено"
        )
    return category

@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_superuser: Annotated[User, Depends(get_current_superuser)]
):
    """
    Оновити категорію за її ID. Доступно лише адміністраторам.
    """
    updated_category = await category_service.update_category(category_id, category_data)
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено"
        )
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    current_superuser: Annotated[User, Depends(get_current_superuser)]
):
    """
    Видалити категорію за її ID. Доступно лише адміністраторам.
    """
    success = await category_service.delete_category(category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категорію з ID {category_id} не знайдено"
        )
    return