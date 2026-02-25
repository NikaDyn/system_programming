import factory
from tests.factories.base import BaseFactory
from tests.factories.place import PlaceFactory
from tests.factories.user import UserFactory
from app.core.models.favorite import Favorite

class FavoriteFactory(BaseFactory):
    class Meta:
        model = Favorite

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)