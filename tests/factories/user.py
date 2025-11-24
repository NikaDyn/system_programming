import factory
from app.core.models.user import User
from tests.factories.base import BaseFactory
from app.core.security import get_password_hash


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    full_name = factory.Faker("name")
    hashed_password = factory.LazyAttribute(lambda o: get_password_hash("password"))
    is_active = True
    is_superuser = False