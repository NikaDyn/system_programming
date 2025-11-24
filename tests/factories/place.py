import factory
from app.core.models.place import Place
from tests.factories.base import BaseFactory
from tests.factories.category import CategoryFactory


class PlaceFactory(BaseFactory):
    class Meta:
        model = Place

    name = factory.Faker("company")
    description = factory.Faker("sentence")
    address = factory.Faker("address")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    is_new = False
    is_popular = False

    category = factory.SubFactory(CategoryFactory)