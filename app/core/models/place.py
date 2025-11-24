from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.models.base import BaseModel


class Place(BaseModel):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_new = Column(Boolean, default=False)
    is_popular = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="places")
    favorites = relationship("Favorite", back_populates="place", cascade="all, delete-orphan")