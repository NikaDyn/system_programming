import factory
from factory import fuzzy
from tests.factories.base import BaseFactory
from app.core.models.category import Category

class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    name = fuzzy.FuzzyChoice(['Food', 'Entertainment', 'Walking', 'Historical', 'Art', 'Nature'])