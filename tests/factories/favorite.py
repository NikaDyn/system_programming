import factory
from . import BaseFactory
from app.core.models.favorite import Favorite
from tests.factories.place import PlaceFactory
from tests.factories.user import UserFactory


class FavoriteFactory(BaseFactory):
    class Meta:
        model = Favorite

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)