from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import List, Annotated, Optional
from pydantic import PositiveInt

from app.schemas.place import PlaceCreate, PlaceRead, PlaceUpdate, PlaceDetailedRead
from app.services.place import PlaceService
from app.dependencies import get_place_service, get_current_active_user, get_category_service
from app.core.models.user import User

router = APIRouter(
    prefix="/places",
    tags=["Places"],
)

@router.post("/", response_model=PlaceRead, status_code=status.HTTP_201_CREATED)
async def create_place(
    place_data: PlaceCreate,
    place_service: Annotated[PlaceService, Depends(get_place_service)],
    # Місце може створити тільки аутентифікований користувач
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Створити нове місце (туристичний об'єкт).
    """
    try:
        new_place = await place_service.create_place(
            place_data=place_data,
            creator_id=current_user.id
        )
        return new_place
    except HTTPException:
        # Перевикидаємо HTTP-виключення, якщо воно прийшло з PlaceService (наприклад, 404 для Category)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Не вдалося створити місце: {e}"
        )

@router.get("/", response_model=List[PlaceRead])
async def search_places(
    place_service: Annotated[PlaceService, Depends(get_place_service)],
    # Параметри фільтрації та пошуку
    search: Optional[str] = Query(None, description="Пошук за назвою або описом"),
    category_id: Optional[PositiveInt] = Query(None, description="Фільтр за ID категорії"),
    limit: PositiveInt = Query(10, le=100, description="Обмеження кількості результатів"),
    offset: int = Query(0, ge=0, description="Зміщення для пагінації")
):
    """
    Пошук та фільтрація місць.
    """
    places = await place_service.search_places(
        search=search,
        category_id=category_id,
        limit=limit,
        offset=offset
    )
    return places

@router.get("/{place_id}", response_model=PlaceDetailedRead)
async def read_place_by_id(
    place_id: PositiveInt,
    place_service: Annotated[PlaceService, Depends(get_place_service)]
):
    """
    Отримати детальну інформацію про місце за його ID.
    """
    place = await place_service.get_place_by_id(place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Місце з ID {place_id} не знайдено"
        )
    return place

@router.patch("/{place_id}", response_model=PlaceRead)
async def update_place(
    place_id: PositiveInt,
    place_data: PlaceUpdate,
    place_service: Annotated[PlaceService, Depends(get_place_service)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Оновити інформацію про місце. Тільки автор або суперкористувач може оновлювати.
    """
    updated_place = await place_service.update_place(
        place_id=place_id,
        place_data=place_data,
        updater_user=current_user
    )
    if updated_place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Місце з ID {place_id} не знайдено або у вас немає прав на оновлення"
        )
    return updated_place

@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place(
    place_id: PositiveInt,
    place_service: Annotated[PlaceService, Depends(get_place_service)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Видалити місце. Тільки автор або суперкористувач може видаляти.
    """
    success = await place_service.delete_place(
        place_id=place_id,
        deleter_user=current_user
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Місце з ID {place_id} не знайдено або у вас немає прав на видалення"
        )
    return