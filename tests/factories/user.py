import factory
from passlib.context import CryptContext
from tests.factories.base import BaseFactory
from app.core.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_HASH = pwd_context.hash("testpassword")


class UserFactory(BaseFactory):
    class Meta:
        model = User

    full_name = factory.Faker('name', locale='uk_UA')
    email = factory.Sequence(lambda n: f"user{n}@test.com")

    hashed_password = DEFAULT_HASH

    is_superuser = factory.Faker('boolean', chance_of_getting_true=5)
    is_active = True