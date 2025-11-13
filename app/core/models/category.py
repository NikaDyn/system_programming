from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    places = relationship("Place", back_populates="category")
