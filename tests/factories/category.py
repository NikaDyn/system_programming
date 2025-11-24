import factory
from app.core.models.category import Category
from tests.factories.base import BaseFactory

class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    # Генеруємо унікальну назву (наприклад: "Restautant", "Park")
    name = factory.Faker("word")
    # Генеруємо опис
    description = factory.Faker("sentence")