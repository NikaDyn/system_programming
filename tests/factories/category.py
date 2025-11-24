import factory
from app.core.models.category import Category
from tests.factories.base import BaseFactory


class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    description = factory.Faker("sentence")
