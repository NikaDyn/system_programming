import factory
from factory.alchemy import SQLAlchemyModelFactory


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'
