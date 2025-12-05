import factory
from factory import fuzzy
from . import BaseFactory
from app.core.models.category import Category


class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    id = factory.Sequence(lambda n: n + 1)
    name = fuzzy.FuzzyChoice(['Food', 'Entertainment', 'Walking', 'Historical', 'Art', 'Nature'])