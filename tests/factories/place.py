import factory
from factory import fuzzy
from . import BaseFactory
from app.core.models.place import Place
from .category import CategoryFactory


class PlaceFactory(BaseFactory):
    class Meta:
        model = Place

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('company', locale='uk_UA')
    description = factory.Faker('paragraph', nb_sentences=3, locale='uk_UA')
    address = factory.Faker('street_address', locale='uk_UA')

    latitude = fuzzy.FuzzyFloat(48.91, 49.00, precision=6)
    longitude = fuzzy.FuzzyFloat(24.69, 24.75, precision=6)

    category = factory.SubFactory(CategoryFactory)

    theme = fuzzy.FuzzyChoice(['Cafe', 'Bar', 'Park', 'Museum', 'Street Food'])

    is_new = factory.Faker('boolean', chance_of_getting_true=20)
    is_popular = factory.Faker('boolean', chance_of_getting_true=50)