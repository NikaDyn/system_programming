import factory
from .base import BaseFactory
from app.core.models.favorite import Favorite
from .place import PlaceFactory
from .user import UserFactory

class FavoriteFactory(BaseFactory):
    class Meta:
        model = Favorite

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)