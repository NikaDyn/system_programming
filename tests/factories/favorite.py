import factory
from app.core.models.favorite import Favorite
from tests.factories.base import BaseFactory
from tests.factories.user import UserFactory
from tests.factories.place import PlaceFactory


class FavoriteFactory(BaseFactory):
    class Meta:
        model = Favorite

    user = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)
