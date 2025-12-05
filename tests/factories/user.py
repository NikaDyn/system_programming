import factory
from factory import fuzzy
from . import BaseFactory
from app.core.models.user import User


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Faker('first_name', locale='uk_UA')
    last_name = factory.Faker('last_name', locale='uk_UA')
    email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}{o.id}@test.com".lower())
    password_hash = "$2b$12$R.S.W3.uGgZ8.Q3Z/x.c.eN.M5f4O2P4tLgD.J2.gY.k.rD7p.G4"
    is_admin = factory.Faker('boolean', chance_of_getting_true=5)
    is_active = True
    is_verified = True