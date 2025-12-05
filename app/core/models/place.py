from app.db import db
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(db):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)

    # !!! НОВЕ ПОЛЕ: Фізична адреса !!!
    address = Column(String)

    # Географічні дані
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Додаткові поля (залишаємо їх у моделі для гнучкості)
    image_url = Column(String)
    is_new = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)

    # Зв'язок з Category (Багато-до-одного)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Зв'язок SQLAlchemy
    category = relationship("Category", back_populates="places")

    # Зворотний зв'язок з 'Favorites'
    favorites = relationship("Favorite", back_populates="place")